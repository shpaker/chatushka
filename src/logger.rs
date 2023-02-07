use env_logger::Builder;
use log::LevelFilter;

pub fn init_logger(debug: bool,) {
    let log_level = match debug {
        true => LevelFilter::Debug,
        false => LevelFilter::Info,
    };
    Builder::new().filter(None, log_level,).init();
}
