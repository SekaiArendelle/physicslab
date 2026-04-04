import time
from physicslab import enums
from physicslab._typing import Optional, Set, List, Dict, Any
from physicslab.errors import ExperimentTypeError
from physicslab._experiment import (
    serialize_introduction,
    deserialize_introduction,
    serialize_tags,
    construct_tags,
)

class Summary:
    """Summary information about an experiment, as displayed in Physics-Lab-AR."""

    __experiment_type: int
    __subject: Optional[str]
    __description: Optional[str]
    __tags: Set[enums.Tag]
    __type_tag: str
    __parent_id: Optional[str]
    __parent_name: Optional[str]
    __parent_category: Optional[str]
    __content_id: Optional[str]
    __editor: Optional[str]
    __coauthors: List[Any]
    __localized_description: Optional[str]
    __model_id: Optional[str]
    __model_name: Optional[str]
    __model_tags: List[str]
    __version: int
    __language: Optional[str]
    __visits: int
    __stars: int
    __supports: int
    __remixes: int
    __comments: int
    __price: int
    __popularity: int
    __creation_date: int
    __update_date: int
    __sorting_date: int
    __summary_id: Optional[str]
    __category: Optional[str]
    __localized_subject: Optional[str]
    __image: int
    __image_region: int
    __user: Dict[str, Any]
    __visibility: int
    __settings: Dict[str, Any]
    __multilingual: bool

    def __init__(
        self,
        experiment_type: int,
        subject: Optional[str],
        description: Optional[str],
        tags: Set[enums.Tag],
        type_tag: str,
        parent_id: Optional[str],
        parent_name: Optional[str],
        parent_category: Optional[str],
        content_id: Optional[str],
        editor: Optional[str],
        coauthors: List[Any],
        localized_description: Optional[str],
        model_id: Optional[str],
        model_name: Optional[str],
        model_tags: List[str],
        version: int,
        language: Optional[str],
        visits: int,
        stars: int,
        supports: int,
        remixes: int,
        comments: int,
        price: int,
        popularity: int,
        creation_date: int,
        update_date: int,
        sorting_date: int,
        summary_id: Optional[str],
        category: Optional[str],
        localized_subject: Optional[str],
        image: int,
        image_region: int,
        user: Dict[str, Any],
        visibility: int,
        settings: Dict[str, Any],
        multilingual: bool,
    ) -> None:
        self.experiment_type = experiment_type
        self.subject = subject
        self.description = description
        self.tags = tags
        self.type_tag = type_tag
        self.parent_id = parent_id
        self.parent_name = parent_name
        self.parent_category = parent_category
        self.content_id = content_id
        self.editor = editor
        self.coauthors = coauthors
        self.localized_description = localized_description
        self.model_id = model_id
        self.model_name = model_name
        self.model_tags = model_tags
        self.version = version
        self.language = language
        self.visits = visits
        self.stars = stars
        self.supports = supports
        self.remixes = remixes
        self.comments = comments
        self.price = price
        self.popularity = popularity
        self.creation_date = creation_date
        self.update_date = update_date
        self.sorting_date = sorting_date
        self.summary_id = summary_id
        self.category = category
        self.localized_subject = localized_subject
        self.image = image
        self.image_region = image_region
        self.user = user
        self.visibility = visibility
        self.settings = settings
        self.multilingual = multilingual

    @property
    def experiment_type(self) -> int:
        return self.__experiment_type

    @experiment_type.setter
    def experiment_type(self, experiment_type: int) -> None:
        if not isinstance(experiment_type, int):
            raise TypeError(
                f"experiment_type must be of type `int`, but got value {experiment_type} of type {type(experiment_type).__name__}"
            )
        self.__experiment_type = experiment_type

    @property
    def subject(self) -> Optional[str]:
        return self.__subject

    @subject.setter
    def subject(self, subject: Optional[str]) -> None:
        if not isinstance(subject, (str, type(None))):
            raise TypeError(
                f"subject must be of type `str | None`, but got value {subject} of type {type(subject).__name__}"
            )
        self.__subject = subject

    @property
    def description(self) -> Optional[str]:
        return self.__description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        if not isinstance(description, (str, type(None))):
            raise TypeError(
                f"description must be of type `str | None`, but got value {description} of type {type(description).__name__}"
            )
        self.__description = description

    @property
    def tags(self) -> Set[enums.Tag]:
        return self.__tags.copy()

    @tags.setter
    def tags(self, tags: Set[enums.Tag]) -> None:
        if not isinstance(tags, set):
            raise TypeError(
                f"tags must be of type `set[Tag]`, but got value {tags} of type {type(tags).__name__}"
            )
        if not all(isinstance(tag, enums.Tag) for tag in tags):
            raise TypeError(
                f"tags must be of type `set[Tag]`, but got value {tags} of type `set` containing non-Tag elements"
            )
        self.__tags = tags.copy()

    @property
    def type_tag(self) -> str:
        return self.__type_tag

    @type_tag.setter
    def type_tag(self, type_tag: str) -> None:
        if not isinstance(type_tag, str):
            raise TypeError(
                f"type_tag must be of type `str`, but got value {type_tag} of type {type(type_tag).__name__}"
            )
        self.__type_tag = type_tag

    @property
    def parent_id(self) -> Optional[str]:
        return self.__parent_id

    @parent_id.setter
    def parent_id(self, parent_id: Optional[str]) -> None:
        self.__parent_id = parent_id

    @property
    def parent_name(self) -> Optional[str]:
        return self.__parent_name

    @parent_name.setter
    def parent_name(self, parent_name: Optional[str]) -> None:
        self.__parent_name = parent_name

    @property
    def parent_category(self) -> Optional[str]:
        return self.__parent_category

    @parent_category.setter
    def parent_category(self, parent_category: Optional[str]) -> None:
        self.__parent_category = parent_category

    @property
    def content_id(self) -> Optional[str]:
        return self.__content_id

    @content_id.setter
    def content_id(self, content_id: Optional[str]) -> None:
        self.__content_id = content_id

    @property
    def editor(self) -> Optional[str]:
        return self.__editor

    @editor.setter
    def editor(self, editor: Optional[str]) -> None:
        self.__editor = editor

    @property
    def coauthors(self) -> List[Any]:
        return list(self.__coauthors)

    @coauthors.setter
    def coauthors(self, coauthors: List[Any]) -> None:
        self.__coauthors = list(coauthors)

    @property
    def localized_description(self) -> Optional[str]:
        return self.__localized_description

    @localized_description.setter
    def localized_description(self, localized_description: Optional[str]) -> None:
        self.__localized_description = localized_description

    @property
    def model_id(self) -> Optional[str]:
        return self.__model_id

    @model_id.setter
    def model_id(self, model_id: Optional[str]) -> None:
        self.__model_id = model_id

    @property
    def model_name(self) -> Optional[str]:
        return self.__model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]) -> None:
        self.__model_name = model_name

    @property
    def model_tags(self) -> List[str]:
        return list(self.__model_tags)

    @model_tags.setter
    def model_tags(self, model_tags: List[str]) -> None:
        self.__model_tags = list(model_tags)

    @property
    def version(self) -> int:
        return self.__version

    @version.setter
    def version(self, version: int) -> None:
        self.__version = version

    @property
    def language(self) -> Optional[str]:
        return self.__language

    @language.setter
    def language(self, language: Optional[str]) -> None:
        self.__language = language

    @property
    def visits(self) -> int:
        return self.__visits

    @visits.setter
    def visits(self, visits: int) -> None:
        self.__visits = visits

    @property
    def stars(self) -> int:
        return self.__stars

    @stars.setter
    def stars(self, stars: int) -> None:
        self.__stars = stars

    @property
    def supports(self) -> int:
        return self.__supports

    @supports.setter
    def supports(self, supports: int) -> None:
        self.__supports = supports

    @property
    def remixes(self) -> int:
        return self.__remixes

    @remixes.setter
    def remixes(self, remixes: int) -> None:
        self.__remixes = remixes

    @property
    def comments(self) -> int:
        return self.__comments

    @comments.setter
    def comments(self, comments: int) -> None:
        self.__comments = comments

    @property
    def price(self) -> int:
        return self.__price

    @price.setter
    def price(self, price: int) -> None:
        self.__price = price

    @property
    def popularity(self) -> int:
        return self.__popularity

    @popularity.setter
    def popularity(self, popularity: int) -> None:
        self.__popularity = popularity

    @property
    def creation_date(self) -> int:
        return self.__creation_date

    @creation_date.setter
    def creation_date(self, creation_date: int) -> None:
        self.__creation_date = creation_date

    @property
    def update_date(self) -> int:
        return self.__update_date

    @update_date.setter
    def update_date(self, update_date: int) -> None:
        self.__update_date = update_date

    @property
    def sorting_date(self) -> int:
        return self.__sorting_date

    @sorting_date.setter
    def sorting_date(self, sorting_date: int) -> None:
        self.__sorting_date = sorting_date

    @property
    def summary_id(self) -> Optional[str]:
        return self.__summary_id

    @summary_id.setter
    def summary_id(self, summary_id: Optional[str]) -> None:
        self.__summary_id = summary_id

    @property
    def category(self) -> Optional[str]:
        return self.__category

    @category.setter
    def category(self, category: Optional[str]) -> None:
        self.__category = category

    @property
    def localized_subject(self) -> Optional[str]:
        return self.__localized_subject

    @localized_subject.setter
    def localized_subject(self, localized_subject: Optional[str]) -> None:
        self.__localized_subject = localized_subject

    @property
    def image(self) -> int:
        return self.__image

    @image.setter
    def image(self, image: int) -> None:
        self.__image = image

    @property
    def image_region(self) -> int:
        return self.__image_region

    @image_region.setter
    def image_region(self, image_region: int) -> None:
        self.__image_region = image_region

    @property
    def user(self) -> Dict[str, Any]:
        return dict(self.__user)

    @user.setter
    def user(self, user: Dict[str, Any]) -> None:
        self.__user = dict(user)

    @property
    def visibility(self) -> int:
        return self.__visibility

    @visibility.setter
    def visibility(self, visibility: int) -> None:
        self.__visibility = visibility

    @property
    def settings(self) -> Dict[str, Any]:
        return dict(self.__settings)

    @settings.setter
    def settings(self, settings: Dict[str, Any]) -> None:
        self.__settings = dict(settings)

    @property
    def multilingual(self) -> bool:
        return self.__multilingual

    @multilingual.setter
    def multilingual(self, multilingual: bool) -> None:
        self.__multilingual = multilingual

    def as_dict(self) -> dict:
        return {
            "Type": self.experiment_type,
            "ParentID": self.__parent_id,
            "ParentName": self.__parent_name,
            "ParentCategory": self.__parent_category,
            "ContentID": self.__content_id,
            "Editor": self.__editor,
            "Coauthors": self.__coauthors,
            "Description": serialize_introduction(self.description),
            "LocalizedDescription": self.__localized_description,
            "Tags": serialize_tags(self.tags, type_tag=self.type_tag),
            "ModelID": self.__model_id,
            "ModelName": self.__model_name,
            "ModelTags": self.__model_tags,
            "Version": self.__version,
            "Language": self.__language,
            "Visits": self.__visits,
            "Stars": self.__stars,
            "Supports": self.__supports,
            "Remixes": self.__remixes,
            "Comments": self.__comments,
            "Price": self.__price,
            "Popularity": self.__popularity,
            "CreationDate": self.__creation_date,
            "UpdateDate": self.__update_date,
            "SortingDate": self.__sorting_date,
            "ID": self.__summary_id,
            "Category": self.__category,
            "Subject": self.subject,
            "LocalizedSubject": self.__localized_subject,
            "Image": self.__image,
            "ImageRegion": self.__image_region,
            "User": self.__user,
            "Visibility": self.__visibility,
            "Settings": self.__settings,
            "Multilingual": self.__multilingual,
        }


def construct_summary_from_plsav_dict(
    summary_dict: Optional[dict],
    experiment_type: int,
    type_tag: str,
) -> Summary:
    if not isinstance(experiment_type, int):
        raise TypeError(
            f"experiment_type must be of type `int`, but got value {experiment_type} of type {type(experiment_type).__name__}"
        )
    if summary_dict is None:
        return Summary(
            experiment_type=experiment_type,
            subject=None,
            description=None,
            tags=set(),
            type_tag=type_tag,
            parent_id=None,
            parent_name=None,
            parent_category=None,
            content_id=None,
            editor=None,
            coauthors=[],
            localized_description=None,
            model_id=None,
            model_name=None,
            model_tags=[],
            version=0,
            language=None,
            visits=0,
            stars=0,
            supports=0,
            remixes=0,
            comments=0,
            price=0,
            popularity=0,
            creation_date=int(time.time() * 1000),
            update_date=0,
            sorting_date=0,
            summary_id=None,
            category=None,
            localized_subject=None,
            image=0,
            image_region=0,
            user={
                "ID": None,
                "Nickname": None,
                "Signature": None,
                "Avatar": 0,
                "AvatarRegion": 0,
                "Decoration": 0,
                "Verification": None,
            },
            visibility=0,
            settings={},
            multilingual=False,
        )
    if not isinstance(summary_dict, dict):
        raise TypeError(
            f"summary_dict must be of type `dict | None`, but got value {summary_dict} of type {type(summary_dict).__name__}"
        )

    return Summary(
        experiment_type=experiment_type,
        subject=summary_dict["Subject"],
        description=deserialize_introduction(summary_dict["Description"]),
        tags=construct_tags(summary_dict["Tags"], type_tag=type_tag),
        type_tag=type_tag,
        parent_id=summary_dict["ParentID"],
        parent_name=summary_dict["ParentName"],
        parent_category=summary_dict["ParentCategory"],
        content_id=summary_dict["ContentID"],
        editor=summary_dict["Editor"],
        coauthors=summary_dict["Coauthors"],
        localized_description=summary_dict["LocalizedDescription"],
        model_id=summary_dict["ModelID"],
        model_name=summary_dict["ModelName"],
        model_tags=summary_dict["ModelTags"],
        version=summary_dict["Version"],
        language=summary_dict["Language"],
        visits=summary_dict["Visits"],
        stars=summary_dict["Stars"],
        supports=summary_dict["Supports"],
        remixes=summary_dict["Remixes"],
        comments=summary_dict["Comments"],
        price=summary_dict["Price"],
        popularity=summary_dict["Popularity"],
        creation_date=summary_dict["CreationDate"],
        update_date=summary_dict["UpdateDate"],
        sorting_date=summary_dict["SortingDate"],
        summary_id=summary_dict["ID"],
        category=summary_dict["Category"],
        localized_subject=summary_dict["LocalizedSubject"],
        image=summary_dict["Image"],
        image_region=summary_dict["ImageRegion"],
        user=summary_dict["User"],
        visibility=summary_dict["Visibility"],
        settings=summary_dict["Settings"],
        multilingual=summary_dict["Multilingual"],
    )
