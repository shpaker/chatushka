pub enum APIMethods {
    GETUPDATES,
    SENDMESSAGE,
}
impl APIMethods {
    pub fn as_string(&self,) -> &'static str {
        match self {
            APIMethods::GETUPDATES => "getupdates",
            APIMethods::SENDMESSAGE => "sendmessage",
        }
    }
}
