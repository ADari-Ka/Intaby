use std::sync::Mutex;

use rocket::{get, post, put, serde::json::Json, State};

use crate::database::{DBAccessor, DBError};

mod games;

use games::*;

type Database = Box<dyn DBAccessor>;
type SResult<T> = Result<T, Error>;
type GamesState = Mutex<Games>;

#[derive(Debug)]
enum Error {
    Database(DBError),
    GameNotFound(GameCode),
    BadRequest,
}

pub async fn rocket(config: rocket::Config, db_uri: &str) -> rocket::Rocket<rocket::Build> {
    let database = crate::database::sql::SqlAccess::new(db_uri)
        .await
        .expect("Failed to access the database");
    rocket::custom(config)
        .manage(Box::new(database) as Database)
        .manage(Mutex::new(Games::new()))
        .mount("/", rocket::routes![index, create_or_join_game, get_game])
}

#[get("/")]
fn index() -> &'static str {
    "This server handles games\n"
}

/// Create a new game from the quiz id
/// or join an existing game with the specified code
#[post("/games/<id>", data = "<name>")]
async fn create_or_join_game(
    id: GameCode,
    name: Option<PlayerName>,
    games: &State<GamesState>,
    database: &State<Database>,
) -> Result<String, Error> {
    match id.parse::<u64>() {
        Ok(quiz_id) => create_game(quiz_id, games, database).await,
        Err(_) => match name {
            Some(name) => join_game(id, name, games).await.map(|()| format!("")),
            None => Err(Error::BadRequest),
        },
    }
}

#[get("/games/<code>")]
async fn get_game(code: GameCode, games: &State<GamesState>) -> SResult<GameCode> {
    match games.lock().unwrap().get_game(&code) {
        Some(_game) => Ok(code),
        None => Err(Error::GameNotFound(code)),
    }
}

#[put("/games/<code>", data = "<answer>")]
async fn game_answer(code: GameCode, answer: Json<GameAnswer>) -> SResult<()> {
    // TODO: register answer
    Ok(())
}

async fn create_game(
    _quiz_id: u64,
    games: &State<GamesState>,
    _database: &State<Database>,
) -> SResult<GameCode> {
    // TODO: query quiz information from the database
    let code = games.lock().unwrap().create_game();
    Ok(code)
}

async fn join_game(
    game_code: GameCode,
    player_name: PlayerName,
    games: &State<GamesState>,
) -> SResult<()> {
    match games.lock().unwrap().get_game_mut(&game_code) {
        None => Err(Error::GameNotFound(game_code)),
        Some(game) => {
            game.player_join(player_name);
            Ok(())
        }
    }
}

impl Error {
    fn status(&self) -> rocket::http::Status {
        use rocket::http::Status;
        match self {
            Self::Database(error) => error.status(),
            Self::GameNotFound(_) => Status::NotFound,
            Self::BadRequest => Status::BadRequest,
        }
    }
}

impl DBError {
    fn status(&self) -> rocket::http::Status {
        use rocket::http::Status;
        match self {
            Self::QuizNotFound(_) => Status::NotFound,
            Self::DBCorrupt(_) => Status::InternalServerError,
            Self::Other(_) => Status::InternalServerError,
        }
    }
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Database(error) => error.fmt(f),
            Self::GameNotFound(msg) => {
                write!(f, "A game with the code \'{msg}\' could not be found")
            }
            Self::BadRequest => write!(f, "Bad request"),
        }
    }
}

impl std::error::Error for Error {}

impl From<DBError> for Error {
    fn from(error: DBError) -> Self {
        Self::Database(error)
    }
}

impl<'r> rocket::response::Responder<'r, 'static> for Error {
    fn respond_to(self, _request: &'r rocket::Request<'_>) -> rocket::response::Result<'static> {
        println!("Encountered an error: {self}");
        Err(self.status())
    }
}
