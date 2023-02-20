use crate::Message;
pub trait Matcher {
    fn is_match(
        &self,
        message: &Message,
    ) -> bool;
}
