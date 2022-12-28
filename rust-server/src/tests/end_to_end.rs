use rocket::{
    http::Status,
    local::asynchronous::{Client, LocalRequest, LocalResponse},
};

use super::*;

#[tokio::test]
async fn test() {
    let config = rocket::Config {
        log_level: rocket::log::LogLevel::Debug,
        address: std::net::Ipv4Addr::new(127, 0, 0, 1).into(),
        port: 8000,
        ..Default::default()
    };
    let rocket = crate::server::rocket(config, "postgresql://test:test@localhost:5432").await;
    let client = Client::tracked(rocket).await.unwrap();

    let response = request(client.get("/")).await;

    assert_eq!(response.status(), Status::Ok);
}

async fn request<'c>(request: LocalRequest<'c>) -> LocalResponse<'c> {
    println!("---\nProcessing: {request:?}");
    let response = request.dispatch().await;
    println!("Got response:\n{response:?}\n---");
    response
}
