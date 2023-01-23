#[derive(Debug,)]
pub struct Settings {
    pub bot_token: String,
}

impl Settings {
    pub fn new() -> Settings {
        Settings {
            bot_token: String::from(
                "5594826653:AAF3lu2j5rjoNdXj6CwL8dfEiDq2iq8H0bI",
            ),
        }
    }
}
