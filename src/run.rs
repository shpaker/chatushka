use clap::Parser;
use log::info;
use regex::Regex;

use super::{
    // read_config,
    ChatListener,
    CliArgs,
    CommandMatcher,
    Matcher,
    MessageAction,
    RegExMatcher,
};
use crate::logger::init_logger;

pub fn run() {
    let cli_args = CliArgs::parse();
    init_logger(cli_args.debug,);
    info!("starting up {}", cli_args.debug);

    // read_config(cli_args.config.as_str(),);
    let matchers: Vec<Box<dyn Matcher,>,> = vec![
        Box::new(CommandMatcher {
            token: "foo",
            case_insensitive: true,
            prefixes: vec!['!'],
            action: Box::new(MessageAction { template: "aa", },),
        },),
        Box::new(RegExMatcher {
            regex: Regex::new(r"^\d{2}$",).unwrap(),
            case_insensitive: true,
            action: Box::new(MessageAction { template: "bb", },),
        },),
    ];
    let listener = ChatListener::new(cli_args.token.as_str(), matchers,);
    match listener.long_polling() {
        Err(err,) => panic!("Error happened {:?}!", err),
        Ok(value,) => value,
    };
}
