pub mod community {
	use serde::{Deserialize, Serialize};
	
	pub enum CommunityVisibility {
		Public,
	}
	pub enum CommunitySubscribed {
		NotSubscribed,
	}

	#[derive(Serialize, Deserialize)]
	pub struct Communities {
		pub communities: Vec<CommunityInfo>,
	}

	#[derive(Serialize, Deserialize)]
	pub struct CommunityInfo {
		pub community: Community,
		pub subscribed: CommunitySubscribed,
		pub blocked: bool,
		pub counts: CommunityCounts,
		pub banned_from_community: bool,
	}

	#[derive(Serialize, Deserialize)]
	pub struct Community {
		pub id: u64,
		pub name: String,
		pub title: String,
		pub description: String,
		pub removed: bool,
		pub published: String,
		pub deleted: bool,
		pub nsfw: bool,
		pub actor_id: String,
		pub local: bool,
		pub icon: String,
		pub banner: String,
		pub hidden: bool,
		pub instance_id: u64,
		pub visibility: CommunityVisibility,
	}

	#[derive(Serialize, Deserialize)]
	pub struct CommunityCounts {
		pub community_id: u64,
		pub subscribers: u64,
		pub posts: u64,
		pub comments: u64,
		pub published: String,
		pub users_active_day: u64,
		pub users_active_week: u64,
		pub users_active_month: u64,
		pub users_active_half_year: u64,
		pub users_active_year: u64,
		pub subscribers_local: u64,
	}
}
