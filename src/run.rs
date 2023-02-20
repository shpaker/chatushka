use clap::Parser;
use log::info;

use super::{
    init_logger,
    Bot,
    CliArgs,
    Config,
};

pub fn run() {
    let cli_args = CliArgs::parse();
    init_logger(cli_args.debug,);
    info!("starting up [debug is {}]", cli_args.debug);
    let bot = Bot::new(cli_args.token.as_str(),);
    let config = match Config::from_file(cli_args.config.as_str(), &bot.rhai_engine,) {
        Err(err,) => panic!("incorrect config: {:?}!", err),
        Ok(value,) => value,
    };
    match bot.run(&config.listeners,) {
        Err(err,) => panic!("error happened: {:?}!", err),
        Ok(value,) => value,
    };
}
