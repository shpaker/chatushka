#[derive(Debug,)]
pub enum BotErrors {
    APIError,
    ConnectionError,
    NotOkResponse,
    IncorrectResponse,
}

#[derive(Debug,)]
pub enum ConfigErrors {
    UnknownMatcherType,
    UnknownActionType,
    MissingValue,
}

#[derive(Debug,)]
pub enum ListenerErrors {
    CompileError,
    CallActionError,
}
