use std::{
    collections::HashMap,
    time::Duration,
};

use reqwest::blocking::Client;
use serde_json::Value;

use super::APIMethods;

#[derive(Debug,)]
pub struct BotAPI {
    api_endpoint: String,
}

impl BotAPI {
    pub fn new(token: &str,) -> BotAPI {
        BotAPI {
            api_endpoint: format!(
                "https://api.telegram.org/bot{}",
                token
            ),
        }
    }

    fn make_url(
        &self,
        method: APIMethods,
    ) -> String {
        format!("{}/{}", self.api_endpoint, method.as_string())
    }

    pub fn api_send(
        &self,
        method: APIMethods,
        data: &HashMap<&str, String,>,
        timeout: u64,
    ) -> Option<Value,> {
        let client = Client::new();
        let url: String = self.make_url(method,);
        match client
            .post(url,)
            .json(&data,)
            .timeout(Duration::from_secs(timeout,),)
            .send()
        {
            Err(_why,) => {
                println!("{:?}", _why);
                return None;
            }
            Ok(resp,) => {
                match resp.text() {
                    Err(_why,) => return None,
                    Ok(result,) => {
                        let response_map: HashMap<String, Value,> =
                            serde_json::from_str(result.as_str(),)
                                .unwrap();
                        if response_map["ok"] != true {
                            return None;
                        }
                        let result_field = &response_map["result"];
                        return Some(result_field.clone(),);
                    }
                };
            }
        };
    }

    pub fn get_updates(
        &self,
        offset: Option<i64,>,
        timeout: u64,
    ) -> Option<Value,> {
        let mut request_data: HashMap<&str, String,> = HashMap::new();
        if !offset.is_none() {
            request_data.insert("offset", offset.unwrap().to_string(),);
        };
        let resp = self.api_send(
            APIMethods::GETUPDATES,
            &request_data,
            timeout,
        );
        return resp;
    }

    pub fn send_message(
        &self,
        chat_id: i64,
        text: &str,
        reply_to_message_id: i64,
        timeout: u64,
    ) -> Option<Value,> {
        let mut request_data = HashMap::from([
            ("chat_id", chat_id.to_string(),),
            ("text", text.to_string(),),
            ("reply_to_message_id", reply_to_message_id.to_string(),),
            ("parse_mode", "html".to_string(),),
        ],);
        // request_data
        let resp = self.api_send(
            APIMethods::SENDMESSAGE,
            &request_data,
            timeout,
        );
        return resp;
    }
}
