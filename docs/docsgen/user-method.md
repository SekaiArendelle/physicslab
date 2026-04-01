
## Ban user
```Python
def ban(self, target_id: str, reason: str, length: int) -> dict
```

Args:
*  target_id: ID of user to be banned
*  reason: Ban reason
*  length: Ban duration in days

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_ban(self, target_id: str, reason: str, length: int) -> Awaitable[dict]
```

## Confirm experiment publication
```Python
def confirm_experiment(self, summary_id: str, category: physicslab.enums.Category, image_counter: int) -> dict
```

Args:
*  summary_id: Summary ID
*  category: Experiment area or black hole area
*  image_counter: Image counter

Returns:
*  dict: Physics-Lab-AR API response structure

Notes:
*  Low-level API, do not use directly
*  Use Experiment.update() and Experiment.upload() methods to publish experiments

async version api:
```Python
async def async_confirm_experiment(self, summary_id: str, category: physicslab.enums.Category, image_counter: int) -> Awaitable[dict]
```

## Follow user
```Python
def follow(self, target_id: str, action: bool = True) -> dict
```

Args:
*  target_id: ID of user to be followed
*  action: true to follow, false to unfollow

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_follow(self, target_id: str, action: bool = True) -> Awaitable[dict]
```

## Get comment board information
```Python
def get_comments(self, target_id: str, target_type: str, take: int = 16, skip: int = 0, comment_id: str | None = None) -> dict
```

Args:
*  target_id: ID of Wushi user / ID of the experiment
*  target_type: User, Discussion, Experiment
*  take: Number of comments to retrieve
*  skip: Number of comments to skip (value is unix timestamp * 1000)
*  comment_id: Retrieve `take` number of messages starting from this comment_id (an alternative skip rule)

Returns:
*  dict: Structure of the response body returned by Wushi API

async version api:
```Python
async def async_get_comments(self, target_id: str, target_type: str, take: int = 16, skip: int = 0, comment_id: str | None = None) -> Awaitable[dict]
```

## Get work details, Physics-Lab-AR uses this interface when reading works for the first time
```Python
def get_derivatives(self, content_id: str, category: physicslab.enums.Category) -> dict
```

Args:
*  content_id: Experiment ID
*  category: Experiment area or black hole area

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_derivatives(self, content_id: str, category: physicslab.enums.Category) -> Awaitable[dict]
```

## Get experiment
```Python
def get_experiment(self, content_id: str, category: physicslab.enums.Category | None = None) -> dict
```

Args:
*  content_id: When category is not None, content_id is experiment ID,
*  otherwise it will be recognized as get_summary()["Data"]["ContentID"] result
*  category: Experiment area or black hole area

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_experiment(self, content_id: str, category: physicslab.enums.Category | None = None) -> Awaitable[dict]
```

## Get community works list
```Python
def get_library(self) -> dict
```

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_library(self) -> Awaitable[dict]
```

## Read system email message
```Python
def get_message(self, message_id: str) -> dict
```

Args:
*  message_id: Message ID

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_message(self, message_id: str) -> Awaitable[dict]
```

## Get messages received by user
```Python
def get_messages(self, category_id: int, skip: int = 0, take: int = 16, no_templates: bool = True) -> dict
```

Args:
*  category_id: Message type:
*  0: All, 1: System email, 2: Followers and fans, 3: Comments and replies, 4: Work notifications, 5: Management records
*  skip: Skip skip messages
*  take: Take take messages
*  no_templates: Whether to not return template messages for message types

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_messages(self, category_id: int, skip: int = 0, take: int = 16, no_templates: bool = True) -> Awaitable[dict]
```

## Get user homepage information
```Python
def get_profile(self) -> dict
```

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_profile(self) -> Awaitable[dict]
```

## Get user's followers/following list
```Python
def get_relations(self, user_id: str, display_type: str = 'Follower', skip: int = 0, take: int = 20, query: str = '') -> dict
```

Args:
*  user_id: User ID
*  display_type: Can only be Follower: followers, Following: following
*  skip: Skip skip users
*  take: Take take users
*  query: User ID or nickname

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_relations(self, user_id: str, display_type: str = 'Follower', skip: int = 0, take: int = 20, query: str = '') -> Awaitable[dict]
```

## Get experiment introduction
```Python
def get_summary(self, content_id: str, category: physicslab.enums.Category) -> dict
```

Args:
*  content_id: Experiment ID
*  category: Experiment area or black hole area

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_summary(self, content_id: str, category: physicslab.enums.Category) -> Awaitable[dict]
```

## Get support list
```Python
def get_supporters(self, content_id: str, category: physicslab.enums.Category, skip: int = 0, take: int = 16) -> dict
```

Args:
*  content_id: Content ID
*  category: .Experiment or .Discussion
*  skip: Pass in a timestamp, skip skip messages
*  take: Take take messages

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_supporters(self, content_id: str, category: physicslab.enums.Category, skip: int = 0, take: int = 16) -> Awaitable[dict]
```

## Get user information
```Python
def get_user(self, msg: str, get_user_mode: physicslab.enums.GetUserMode) -> dict
```

Args:
*  msg: User ID/Username
*  get_user_mode: Get user information by ID/Username

Returns:
*  dict: Physics-Lab-AR API response structure

Notes:
*  Only for compatibility, use `get_user_by_id` or `get_user_by_name` is recommended

async version api:
```Python
async def async_get_user(self, msg: str, get_user_mode: physicslab.enums.GetUserMode) -> Awaitable[dict]
```

## Get user information
```Python
def get_user_by_id(self, id: str) -> dict
```

Args:
*  id: User ID

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_user_by_id(self, id: str) -> Awaitable[dict]
```

## Get user information
```Python
def get_user_by_name(self, name: str) -> dict
```

Args:
*  name: Username

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_get_user_by_name(self, name: str) -> Awaitable[dict]
```

## Modify user signature
```Python
def modify_information(self, target: str) -> dict
```

Args:
*  target: New signature

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_modify_information(self, target: str) -> Awaitable[dict]
```

## Post comment
```Python
def post_comment(self, target_id: str, target_type: str, content: str, reply_id: str | None = None, special: str | None = None) -> dict
```

Args:
*  target_id: Target user/experiment ID
*  target_type: User, Discussion, Experiment
*  content: Comment content
*  reply_id: ID of user being replied to (can be automatically derived)
*  special: "Reminder" for sending warning, None for normal comment

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_post_comment(self, target_id: str, target_type: str, content: str, reply_id: str | None = None, special: str | None = None) -> Awaitable[dict]
```

## Query experiments
```Python
def query_experiments(self, category: physicslab.enums.Category, tags: List[physicslab.enums.Tag] | None = None, exclude_tags: List[physicslab.enums.Tag] | None = None, languages: List[str] | None = None, exclude_languages: List[str] | None = None, user_id: str | None = None, take: int = 20, skip: int = 0, from_skip: str | None = None) -> dict
```

Args:
*  category: Experiment area or black hole area
*  tags: Search for experiments with corresponding Physics-Lab-AR experiment tags in the list
*  exclude_tags: All experiments except those with tags in the list will be searched
*  languages: Search for experiments with corresponding languages in the list
*  exclude_languages: All experiments except those with languages in the list will be searched
*  user_id: Specify the publisher of the works to search for
*  take: Number of searches
*  skip: Number of searches to skip
*  from_skip: Starting position identifier

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_query_experiments(self, category: physicslab.enums.Category, tags: List[physicslab.enums.Tag] | None = None, exclude_tags: List[physicslab.enums.Tag] | None = None, languages: List[str] | None = None, exclude_languages: List[str] | None = None, user_id: str | None = None, take: int = 20, skip: int = 0, from_skip: str | None = None) -> Awaitable[dict]
```

## Claim daily check-in reward
```Python
def receive_bonus(self, activity_id: str, index: int) -> dict
```

Args:
*  activity_id: Activity ID
*  index: Which reward of the activity

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_receive_bonus(self, activity_id: str, index: int) -> Awaitable[dict]
```

## Delete comment
```Python
def remove_comment(self, comment_id: str, target_type: str) -> dict
```

Args:
*  comment_id: Comment ID, can be obtained through `get_comments`
*  target_type: User, Discussion, Experiment

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_remove_comment(self, comment_id: str, target_type: str) -> Awaitable[dict]
```

## Hide experiment
```Python
def remove_experiment(self, summary_id: str, category: physicslab.enums.Category, reason: str | None = None) -> dict
```

Args:
*  summary_id: Experiment ID
*  category: Experiment area or black hole area
*  reason: Reason for hiding

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_remove_experiment(self, summary_id: str, category: physicslab.enums.Category, reason: str | None = None) -> Awaitable[dict]
```

## Change user nickname
```Python
def rename(self, nickname: str) -> dict
```

Args:
*  nickname: New nickname

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_rename(self, nickname: str) -> Awaitable[dict]
```

## Favorite/Support an experiment
```Python
def star_content(self, content_id: str, category: physicslab.enums.Category, star_type: int, status: bool = True) -> dict
```

Args:
*  content_id: Experiment ID
*  category: Experiment area, Black hole area
*  star_type: 0: Favorite, 1: Support experiment with gold coins
*  status: True: Favorite, False: Unfavorite (no effect on support)

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_star_content(self, content_id: str, category: physicslab.enums.Category, star_type: int, status: bool = True) -> Awaitable[dict]
```

## Unban user
```Python
def unban(self, target_id: str, reason: str) -> dict
```

Args:
*  target_id: ID of user to be unbanned
*  reason: Unban reason

Returns:
*  dict: Physics-Lab-AR API response structure

async version api:
```Python
async def async_unban(self, target_id: str, reason: str) -> Awaitable[dict]
```

## Upload experiment image
```Python
def upload_image(self, policy: str, authorization: str, image_path: str) -> dict
```

Args:
*  authorization: Can be obtained through /Contents/SubmitExperiment["Data"]["Token"]["Policy"]
*  policy: Can be obtained through /Contents/SubmitExperiment["Data"]["Token"]["Policy"]
*  image_path: Local path of image to be uploaded

Returns:
*  dict: Physics-Lab-AR API response structure

Notes:
*  This API is a low-level API, it is recommended to use the more complete Experiment.upload() and Experiment.update() methods for uploading images

async version api:
```Python
async def async_upload_image(self, policy: str, authorization: str, image_path: str) -> Awaitable[dict]
```
