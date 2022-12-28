use super::*;

use sqlx::AnyPool;

/// Handles access to the postgres games database
pub struct SqlAccess {
    pool: AnyPool,
}

impl SqlAccess {
    /// Sets up access to the database and initializes all the neccessary tables
    pub async fn new(db_uri: &str) -> DBResult<Self> {
        let pool = DBPool::connect(db_uri).await?;
        let sql = Self { pool }.init().await?;
        Ok(sql)
    }

    /// Initialize all the neccessary database stuff
    async fn init(self) -> DBResult<Self> {
        Ok(self)
    }
}

#[async_trait]
impl DBAccessor for SqlAccess {}

impl From<sqlx::Error> for DBError {
    fn from(error: sqlx::Error) -> Self {
        Self::Other(Box::new(error))
    }
}
