use crate::{
    BotAPI,
    Message,
};

pub trait Action {
    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
    );
}
