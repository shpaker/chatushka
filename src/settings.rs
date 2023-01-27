#[derive(Debug,)]
pub struct Settings {
    pub bot_token: String,
}

impl Settings {
    pub fn new() -> Settings {
        Settings {
            bot_token: String::from(
                "5594826653:***",
            ),
        }
    }
}
