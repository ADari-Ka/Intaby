use async_trait::async_trait;
pub use sqlx::any::AnyPool as DBPool;

pub mod sql;

pub type QuizId = u64;

/// The type of error that may occur when interacting
/// with the database
#[derive(Debug)]
pub enum DBError {
    /// A game could not be created because another
    /// with confliting properties already exists
    QuizNotFound(QuizId),
    /// The database is corrupted and could not be
    /// processed properly
    DBCorrupt(String),
    /// Some other error occured
    Other(Box<dyn std::error::Error>),
}

pub type DBResult<T> = Result<T, DBError>;

/// Trait representing a handler for the database
#[async_trait]
pub trait DBAccessor: Send + Sync {}

impl std::fmt::Display for DBError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::QuizNotFound(id) => write!(f, "Failed to find a quiz with id: {id}"),
            Self::DBCorrupt(msg) => write!(f, "Database is corrupted: {msg}"),
            Self::Other(error) => error.fmt(f),
        }
    }
}

impl std::error::Error for DBError {}
