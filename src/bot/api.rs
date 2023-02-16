use std::{
    collections::HashMap,
    time::Duration,
};

use reqwest::{
    blocking::Client,
    StatusCode,
};
use serde_json::Value;

use crate::BotErrors;

enum APIMethods {
    GETUPDATES,
    SENDMESSAGE,
}
impl APIMethods {
    fn as_str(&self,) -> &'static str {
        match self {
            APIMethods::GETUPDATES => "GetUpdates",
            APIMethods::SENDMESSAGE => "SendMessage",
        }
    }
}

pub struct BotAPI {
    api_endpoint: String,
}

impl BotAPI {
    pub fn new(token: &str,) -> BotAPI {
        BotAPI {
            api_endpoint: format!("https://api.telegram.org/bot{}", token,),
        }
    }

    fn make_url(
        &self,
        method: APIMethods,
    ) -> String {
        format!("{}/{}", self.api_endpoint, method.as_str())
    }

    fn api_send(
        &self,
        method: APIMethods,
        data: &HashMap<&str, String,>,
        timeout: u64,
    ) -> Result<Value, BotErrors,> {
        let client = Client::new();
        let url: String = self.make_url(method,);
        let response = match client
            .post(url,)
            .json(&data,)
            .timeout(Duration::from_secs(timeout,),)
            .send()
        {
            Ok(response,) => response,
            Err(_err,) => return Err(BotErrors::ConnectionError,),
        };
        if response.status() != StatusCode::OK {
            return Err(BotErrors::APIError,);
        }
        let str_data = match response.text() {
            Ok(str_data,) => str_data,
            Err(_err,) => return Err(BotErrors::IncorrectResponse,),
        };
        let response_map: HashMap<String, Value,> =
            serde_json::from_str(str_data.as_str(),).unwrap();
        if response_map["ok"] != true {
            return Err(BotErrors::NotOkResponse,);
        }
        let result_field = &response_map["result"];
        Ok(result_field.clone(),)
    }

    pub fn get_updates(
        &self,
        offset: Option<i64,>,
        timeout: u64,
    ) -> Result<Value, BotErrors,> {
        let mut request_data: HashMap<&str, String,> =
            HashMap::from([("timeout", timeout.to_string(),),],);
        if !offset.is_none() {
            request_data.insert("offset", offset.unwrap().to_string(),);
        };
        let response =
            self.api_send(APIMethods::GETUPDATES, &request_data, timeout,)?;
        Ok(response,)
    }

    pub fn send_message(
        &self,
        chat_id: i64,
        text: &str,
        reply_to_message_id: i64,
        timeout: u64,
    ) -> Result<Value, BotErrors,> {
        let request_data = HashMap::from([
            ("chat_id", chat_id.to_string(),),
            ("text", text.to_string(),),
            ("reply_to_message_id", reply_to_message_id.to_string(),),
            ("parse_mode", "html".to_string(),),
        ],);
        let response =
            self.api_send(APIMethods::SENDMESSAGE, &request_data, timeout,)?;
        Ok(response,)
    }
}
