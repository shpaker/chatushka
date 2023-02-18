use clap::Parser;
use log::info;
use rhai::{
    Engine,
    EvalAltResult,
};

use super::{
    read_config,
    ChatListener,
    CliArgs,
};
use crate::logger::init_logger;

pub fn run() {
    let cli_args = CliArgs::parse();
    init_logger(cli_args.debug,);
    info!("starting up {}", cli_args.debug);
    let matchers = match read_config(cli_args.config.as_str(),) {
        Err(err,) => panic!("Incorrect config: {:?}!", err),
        Ok(value,) => value,
    };
    let listener = ChatListener::new(cli_args.token.as_str(), matchers,);
    match listener.long_polling() {
        Err(err,) => panic!("Error happened: {:?}!", err),
        Ok(value,) => value,
    };
}
