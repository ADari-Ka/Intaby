pub use rocket::serde;
pub use rocket::serde::json::serde_json;
use rocket::{
    serde::{Deserialize, Serialize},
    time::Instant,
};
use std::collections::HashMap;

pub type UserId = u64;
pub type QuizId = u64;
pub type QuestionId = u64;
pub type Time = u64;

#[derive(Debug)]
pub struct Games {
    map: HashMap<GameCode, Game>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(crate = "rocket::serde", deny_unknown_fields)]
pub struct QuizConfig {
    pub name: String,
    pub questions: Vec<Question>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(crate = "rocket::serde", deny_unknown_fields)]
pub enum QuestionType {
    Poll,
    Quiz,
    Multiquiz,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(crate = "rocket::serde", deny_unknown_fields)]
pub struct Question {
    pub answers: Vec<Answer>,
    pub question_type: QuestionType,
    pub quiz_id: QuizId,
    pub text: String,
    pub time: Time,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(crate = "rocket::serde", deny_unknown_fields)]
pub struct Answer {
    pub correct_answer: bool,
    pub question_id: QuestionId,
    pub text: String,
}

/// Represents different states of a game
#[derive(Debug)]
pub enum GameState {
    /// Initial state of the game
    Lobby,
    InProgress {
        current_question: usize,
        current_answers: HashMap<UserId, GameAnswer>,
        start_time: Instant,
    },
    Finished,
}

pub type GameCode = String;
pub type PlayerName = String;

#[derive(Debug, Serialize, Deserialize)]
#[serde(crate = "rocket::serde")]
pub struct Player {
    user_id: UserId,
    name: PlayerName,
}

#[derive(Debug)]
pub struct Game {
    players: HashMap<UserId, Player>,
    quiz_config: QuizConfig,
    state: GameState,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(crate = "rocket::serde", deny_unknown_fields)]
pub struct GameAnswer {
    user_id: UserId,
    question_id: QuestionId,
    answers: Vec<String>,
}

impl Games {
    pub fn new() -> Self {
        Self {
            map: HashMap::new(),
        }
    }

    pub fn create_game(&mut self, quiz_config: QuizConfig) -> GameCode {
        let code = loop {
            let code = game_code_generator();
            if !self.map.contains_key(&code) {
                break code;
            }
        }; // TODO: avoid infinite loop
        let game = Game::new(quiz_config);
        let res = self.map.insert(code.clone(), game);
        assert!(res.is_none());
        code
    }

    pub fn get_game(&self, code: &GameCode) -> Option<&Game> {
        self.map.get(code)
    }

    pub fn get_game_mut(&mut self, code: &GameCode) -> Option<&mut Game> {
        self.map.get_mut(code)
    }
}

impl Game {
    pub fn new(quiz_config: QuizConfig) -> Self {
        Self {
            players: HashMap::new(),
            quiz_config,
            state: GameState::Lobby,
        }
    }

    pub fn player_join(&mut self, player: Player) {
        // TODO: check collisions
        self.players.insert(player.user_id, player);
    }

    pub fn player_answer(&mut self, answer: GameAnswer) {
        self.update();
        match &mut self.state {
            GameState::InProgress {
                current_answers, ..
            } => {
                current_answers.insert(answer.user_id, answer);
            }
            _ => {}
        }
    }

    fn update(&mut self) {
        match &mut self.state {
            GameState::Lobby => {}
            GameState::InProgress {
                current_question,
                current_answers,
                start_time,
            } => {
                let elapsed = start_time.elapsed().as_seconds_f64().floor() as Time;
                let time_limit = self
                    .quiz_config
                    .questions
                    .get(*current_question)
                    .expect("Current question index is illegal")
                    .time;
                if elapsed >= time_limit {
                    if *current_question + 1 >= self.quiz_config.questions.len() {
                        self.state = GameState::Finished;
                    } else {
                        *current_question += 1;
                    }
                }
            }
            GameState::Finished => {}
        }
    }
}

pub fn game_code_generator() -> GameCode {
    use rand::Rng;
    const LEN: usize = 4;

    let mut rng = rand::thread_rng();
    let mut code = String::new();
    for _ in 0..LEN {
        let symbol = rng.gen_range('A'..='Z');
        code.push(symbol);
    }
    code
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_game_create() {
        let mut games = Games::new();
        const CODE_GENS: usize = 1000;
        let quiz = QuizConfig {
            name: "Cool quiz".to_owned(),
            questions: vec![],
        };
        let mut codes = (0..CODE_GENS)
            .map(|_| games.create_game(quiz.clone()))
            .collect::<Vec<_>>();
        codes.sort();
        codes.dedup();
        assert_eq!(CODE_GENS, codes.len())
    }
}
