#[derive(Debug,)]
pub enum BotErrors {
    APIError,
    ConnectionError,
    NotOkResponse,
    IncorrectResponse,
}
