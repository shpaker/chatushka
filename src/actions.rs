use super::{
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

pub struct MessageAction {
    pub template: String,
}

impl Action for MessageAction {
    fn call(
        &self,
        api: &BotAPI,
        message: &Message,
    ) {
        let _ =
            api.send_message(message.chat_id, self.template.as_str(), message.id, 16,);
    }
}
