use clap::Parser;
use env_logger::Builder;
use log::{
    info,
    LevelFilter,
};

use super::{
    BotAPI,
    ChatListener,
    CliArgs,
    Message,
    RegExMatcher,
};

fn test_cb(
    api: &BotAPI,
    message: &Message,
) {
    let result = api.send_message(message.chat_id, "meow", message.id, 16,);
    result.ok();
}

pub fn run() {
    Builder::new().filter(None, LevelFilter::Info,).init();
    let cli_args = CliArgs::parse();
    info!("starting up {}", cli_args.debug);
    let matchers = vec![RegExMatcher::new(r"^(test).*$", test_cb,)];
    let listener = ChatListener::new(cli_args.token.as_str(), &matchers,);
    match listener.long_polling() {
        Err(err,) => panic!("Error happened {:?}!", err),
        Ok(value,) => value,
    };
}
