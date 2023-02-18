pub use config::read_config;
pub use logger::init_logger;
pub use run::run;

mod actions;
mod bot;
mod cli_args;
mod config;
mod errors;
mod logger;
mod matchers;
mod run;

pub(crate) use crate::{
    actions::{
        Action,
        MessageAction,
        RhaiAction,
    },
    bot::{
        BotAPI,
        ChatListener,
        Message,
    },
    cli_args::CliArgs,
    errors::{
        BotErrors,
        ConfigErrors,
    },
    matchers::{
        CommandMatcher,
        Matcher,
        RegExMatcher,
    },
};
