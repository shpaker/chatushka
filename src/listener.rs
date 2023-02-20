use super::{
    Action,
    Matcher,
};

pub struct Listener {
    pub matcher: Box<dyn Matcher,>,
    pub action: Box<dyn Action,>,
    pub data: Vec<String,>,
}
