use clap::Parser;
use log::info;

use super::{
    read_config,
    BotAPI,
    ChatListener,
    CliArgs,
    Message,
    RegExMatcher,
};
use crate::logger::init_logger;

fn test_cb(
    api: &BotAPI,
    message: &Message,
) {
    let result = api.send_message(message.chat_id, "meow", message.id, 16,);
    result.ok();
}

pub fn run() {
    let cli_args = CliArgs::parse();
    init_logger(cli_args.debug,);
    info!("starting up {}", cli_args.debug);

    read_config(cli_args.config.as_str(),);

    let matchers = vec![RegExMatcher::new(r"^(test).*$", test_cb,)];
    let listener = ChatListener::new(cli_args.token.as_str(), &matchers,);
    match listener.long_polling() {
        Err(err,) => panic!("Error happened {:?}!", err),
        Ok(value,) => value,
    };
}
