#[path = "types.rs"]
mod types;
// use reqwest::Error as ReqError;

pub mod communities {
	#[allow(non_snake_case)]
	pub mod list {
    use reqwest::Error;
		pub async fn Hot(instance: &str) -> Result<types::community::Communities, Error> {
			let list = reqwest::get(format!("https://{instance}/api/v3/community/list?sort=Hot"))
				.await?
				.text()
				.await?;

			serde_json::from_str(&list).unwrap()
		}
	}
}
