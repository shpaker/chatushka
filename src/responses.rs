#[derive(Debug,)]
pub struct Message {
    pub update_id: i64,
    pub id: i64,
    pub chat_id: i64,
    pub text: String,
}
