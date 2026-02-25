import typing
from typing import Callable, List, Optional, Type, Union
from dataclasses import dataclass
from enum import Enum
import datetime

from flet import (
    AlertDialog,
    Column,
    Card,
    FontWeight,
    IconButton,
    Container,
    Dropdown,
    ElevatedButton,
    FilledButton,
    GridView,
    Icon,
    Image,
    PopupMenuButton,
    PopupMenuItem,
    ProgressBar,
    ButtonStyle,
    margin,
    NavigationRail,
    ResponsiveRow,
    Row,
    Text,
    TextField,
    TextStyle,
    Control,
    alignment,
    border_radius,
    dropdown,
    icons,
    padding,
    Text,
)

from ..res import colors, dimens, fonts, image_paths

from .abstractions import DialogHandler, TView, TViewParams
from . import utils
from ..res import res_utils


class Spacer(Container):
    """Creates a space between controls"""

    # FIXME: Unpythonic code, replace with
    # class Spacer(Container):
    #     SPACE_SIZES = {
    #         'lg': 40,
    #         'md': 20,
    #         'sm': 10,
    #         'xs': 5,
    #         None: 15,
    #     }

    #     def __init__(self, size=None, **kwargs):
    #         self._space_size = self.SPACE_SIZES[size]
    #         super().__init__(height=self._space_size, width=self._space_size, **kwargs)

    def __init__(
        self,
        lg_space: bool = False,
        md_space: bool = False,
        sm_space: bool = False,
        xs_space: bool = False,
        default_space: int = dimens.SPACE_STD,
    ):
        self._space_size = (
            dimens.SPACE_LG
            if lg_space
            else dimens.SPACE_MD
            if md_space
            else dimens.SPACE_SM
            if sm_space
            else dimens.SPACE_XS
            if xs_space
            else default_space
        )
        super().__init__(
            height=self._space_size, width=self._space_size, padding=0, margin=0
        )


class THeading(Text):
    """Creates a standard heading"""

    def __init__(
        self,
        title: str = "",
        size: int = fonts.SUBTITLE_1_SIZE,
        color: Optional[str] = None,
        align: str = utils.TXT_ALIGN_LEFT,
        show: bool = True,
        expand: bool | int | None = None,
    ):
        """Displays text formatted as a headline"""
        super().__init__(
            title,
            font_family=fonts.HEADLINE_FONT,
            weight=fonts.BOLD_FONT,
            size=size,
            color=color,
            text_align=align,
            visible=show,
            expand=expand,
        )


class TSubHeading(Text):
    """Creates a standard subheading"""

    def __init__(
        self,
        subtitle: str = "",
        size: int = fonts.SUBTITLE_2_SIZE,
        color: Optional[str] = None,
        align: str = utils.TXT_ALIGN_LEFT,
        show: bool = True,
        expand: bool | int | None = None,
    ):
        super().__init__(
            subtitle,
            font_family=fonts.HEADLINE_FONT,
            size=size,
            color=color,
            text_align=align,
            visible=show,
            expand=expand,
        )


class THeadingWithSubheading(Column):
    """Creates a standard heading with a subheading"""

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        alignment_in_container: str = utils.START_ALIGNMENT,
        txt_alignment: str = utils.TXT_ALIGN_LEFT,
        title_size: int = fonts.SUBTITLE_1_SIZE,
        subtitle_size: int = fonts.SUBTITLE_2_SIZE,
        subtitle_color: Optional[str] = None,
    ):

        super().__init__(
            spacing=0,
            horizontal_alignment=alignment_in_container,
            controls=[
                THeading(
                    title=title,
                    size=title_size,
                    align=txt_alignment,
                ),
                TSubHeading(
                    subtitle=subtitle,
                    size=subtitle_size,
                    align=txt_alignment,
                    color=subtitle_color,
                ),
            ],
        )


class TBodyText(Text):
    """Creates a standard body text"""

    def __init__(
        self,
        txt: str = "",
        size: int = fonts.BODY_1_SIZE,
        color: Optional[str] = None,
        show: bool = True,
        col: Optional[dict] = None,
        align: str = utils.TXT_ALIGN_LEFT,
        **kwargs,
    ):
        super().__init__(
            col=col,
            value=txt,
            color=color,
            size=size,
            visible=show,
            text_align=align,
            **kwargs,
        )


class TTextField(TextField):
    """Creates a standard text field"""

    def __init__(
        self,
        on_change: typing.Optional[Callable] = None,
        label: str = "",
        hint: str = "",
        keyboard_type: str = utils.KEYBOARD_TEXT,
        on_focus: typing.Optional[Callable] = None,
        initial_value: typing.Optional[str] = None,
        expand: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
        show: bool = True,
    ):
        """Displays commonly used text field in app forms"""
        txtFieldPad = padding.symmetric(horizontal=dimens.SPACE_XS)

        super().__init__(
            label=label,
            keyboard_type=keyboard_type,
            content_padding=txtFieldPad,
            hint_text=hint,
            hint_style=TextStyle(size=fonts.CAPTION_SIZE),
            value=initial_value,
            focused_border_width=1,
            on_focus=on_focus,
            on_change=on_change,
            password=keyboard_type == utils.KEYBOARD_PASSWORD,
            expand=expand,
            width=width,
            disabled=keyboard_type == utils.KEYBOARD_NONE,
            text_size=fonts.BODY_1_SIZE,
            label_style=TextStyle(size=fonts.BODY_2_SIZE),
            error_style=TextStyle(size=fonts.BODY_2_SIZE, color=colors.ERROR_COLOR),
            visible=show,
        )


class TMultilineField(TextField):
    """Creates a standard multiline text field"""

    def __init__(
        self,
        on_change: typing.Optional[Callable] = None,
        label: str = "",
        hint: str = "",
        on_focus: typing.Optional[Callable] = None,
        keyboardType: str = utils.KEYBOARD_MULTILINE,
        minLines: int = 3,
        maxLines: int = 5,
    ):
        txtFieldHintStyle = TextStyle(size=fonts.CAPTION_SIZE)

        super().__init__(
            label=label,
            keyboard_type=keyboardType,
            hint_text=hint,
            hint_style=txtFieldHintStyle,
            focused_border_width=1,
            min_lines=minLines,
            max_lines=maxLines,
            on_focus=on_focus,
            on_change=on_change,
            text_size=fonts.BODY_1_SIZE,
            label_style=TextStyle(size=fonts.BODY_2_SIZE),
            error_style=TextStyle(size=fonts.BODY_2_SIZE, color=colors.ERROR_COLOR),
        )


class TErrorText(TBodyText):
    """Displays text formatted for errors / warnings"""

    def __init__(
        self,
        txt: str,
        show: bool = True,
    ):
        super().__init__(txt, color=colors.ERROR_COLOR, show=show)


class TPrimaryButton(FilledButton):
    """A button with primary styling"""

    def __init__(
        self,
        on_click: Optional[Callable] = None,
        label: str = "",
        width: int = 200,
        icon: Optional[str] = None,
        show: bool = True,
    ):
        super().__init__(label, width=width, on_click=on_click, icon=icon, visible=show)


class TSecondaryButton(ElevatedButton):
    """A button with secondary styling"""

    def __init__(
        self,
        on_click: Optional[Callable] = None,
        label: str = "",
        width: int = 200,
        icon: Optional[str] = None,
    ):

        super().__init__(
            label,
            width=width,
            on_click=on_click,
            icon=icon,
        )


class TDangerButton(ElevatedButton):
    """A button styled for dangerous actions e.g. delete"""

    def __init__(
        self,
        on_click: Optional[Callable] = None,
        label: str = "",
        width: int = 200,
        icon: Optional[str] = None,
        tooltip: Optional[str] = None,
    ):

        super().__init__(
            text=label,
            color=colors.DANGER_COLOR,
            width=width,
            on_click=on_click,
            icon=icon,
            icon_color=colors.DANGER_COLOR,
            tooltip=tooltip,
        )


class TProfilePhotoImg(Image):
    """Creates a profile photo image"""

    def __init__(
        self,
        pic_src: str = image_paths.default_avatar,
    ):
        super().__init__(
            src=pic_src,
            width=72,
            height=72,
            border_radius=border_radius.all(36),
            fit=utils.CONTAIN,
        )


class TImage(Container):
    """Creates a standard image wrapped in a container"""

    def __init__(
        self,
        path: str,
        semantic_label: str,
        width: int,
    ):
        super().__init__(
            width=width,
            content=Image(src=path, fit=utils.CONTAIN, semantics_label=semantic_label),
        )


class TProgressBar(ProgressBar):
    """Creates a standard progress bar"""

    def __init__(
        self,
        show: bool = True,
    ):
        super().__init__(width=320, height=4, visible=show)


class TDropDown(Column):
    """Creates a standard dropdown button"""

    def __init__(
        self,
        label: str,
        on_change: Optional[Callable] = None,
        items: List[str] = [],
        hint: Optional[str] = "",
        width: Optional[int] = None,
        initial_value: Optional[str] = None,
        show: bool = True,
    ):
        super().__init__()
        self.visible = show
        self.label = label
        self.on_change = on_change
        self.initial_value = initial_value
        self.width = width
        self.hint = hint
        self.options = []
        for item in items:
            self.options.append(
                dropdown.Option(
                    text=item,
                )
            )

    def update_dropdown_items(self, items: List[str]):
        """Updates the dropdown items"""
        self.options.clear()
        for item in items:
            self.options.append(
                dropdown.Option(
                    text=item,
                )
            )
        self.drop_down.options = self.options
        self.update()

    def update_value(
        self,
        new_value: str,
    ):
        """Updates the dropdown value"""
        self.drop_down.value = new_value
        self.drop_down.error_text = None  # clear error text
        self.update()

    @property
    def value(self):
        """Returns the dropdown value"""
        return self.drop_down.value

    def update_error_txt(self, error_txt: str = ""):
        """Updates Or clears the error text"""
        self.drop_down.error_text = error_txt if error_txt else None
        self.update()

    def build(self):
        self.drop_down = Dropdown(
            label=self.label,
            hint_text=self.hint,
            options=self.options,
            text_size=fonts.BODY_1_SIZE,
            label_style=TextStyle(size=fonts.BODY_2_SIZE),
            on_change=self.on_change,
            width=self.width,
            value=self.initial_value,
            content_padding=padding.all(dimens.SPACE_XS),
            error_style=TextStyle(size=fonts.BODY_2_SIZE, color=colors.ERROR_COLOR),
            visible=self.visible,
        )
        return self.drop_down


class DateSelector(Container):
    """Date selector."""

    def __init__(
        self,
        label: str,
        initial_date: Optional[datetime.date] = None,
        label_color: Optional[str] = None,
    ):
        super().__init__()
        self.label = label
        self.initial_date = initial_date if initial_date else datetime.date.today()
        self.date = str(self.initial_date.day)
        self.month = str(self.initial_date.month)
        self.year = str(self.initial_date.year)
        self.label_color = label_color

        self.day_dropdown = TDropDown(
            label="Day",
            hint="",
            on_change=self.on_date_set,
            items=[str(day) for day in range(1, 32)],
            width=50,
            initial_value=self.date,
        )

        self.month_dropdown = TDropDown(
            label="Month",
            on_change=self.on_month_set,
            items=[str(month) for month in range(1, 13)],
            width=50,
            initial_value=self.month,
        )

        self.year_dropdown = TDropDown(
            label="Year",
            on_change=self.on_year_set,
            # set items to a list of years -10 to + 10 years from now
            items=[
                str(year)
                for year in range(
                    datetime.date.today().year - 10, datetime.date.today().year + 10
                )
            ],
            width=100,
            initial_value=self.year,
        )

    def on_date_set(self, e):
        self.date = e.control.value

    def on_month_set(self, e):
        self.month = e.control.value

    def on_year_set(self, e):
        self.year = e.control.value

    def build(self):
        self.content = Column(
            controls=[
                TBodyText(txt=self.label, color=self.label_color),
                Row(
                    [
                        self.day_dropdown,
                        self.month_dropdown,
                        self.year_dropdown,
                    ],
                ),
            ]
        )

    def set_date(self, date: Optional[datetime.date] = None):
        if date is None:
            return
        self.date = str(date.day)
        self.month = str(date.month)
        self.year = str(date.year)
        self.day_dropdown.update_value(self.date)
        self.month_dropdown.update_value(self.month)
        self.year_dropdown.update_value(self.year)

        self.update()

    def get_date(self) -> Optional[datetime.date]:
        """Return the selected timeframe."""
        if self.year is None or self.month is None or self.date is None:
            return None

        date = datetime.date(
            year=int(self.year),
            month=int(self.month),
            day=int(self.date),
        )
        return date


class ConfirmDisplayPopUp(DialogHandler):
    """Pop up used for displaying confirmation pop up"""

    def __init__(
        self,
        dialog_controller: Callable[[any, utils.AlertDialogControls], None],
        title: str,
        description: str,
        on_proceed: Callable,
        data_on_confirmed: Optional[any] = None,
        on_cancel: Optional[Callable] = None,
        proceed_button_label: str = "Proceed",
        cancel_button_label: str = "Cancel",
    ):
        pop_up_height = 150
        dialog = AlertDialog(
            content=Container(
                height=pop_up_height,
                content=Column(
                    scroll=utils.AUTO_SCROLL,
                    controls=[
                        THeading(
                            title=title,
                            size=fonts.HEADLINE_4_SIZE,
                        ),
                        Spacer(xs_space=True),
                        TBodyText(
                            txt=description,
                            size=fonts.SUBTITLE_1_SIZE,
                        ),
                    ],
                ),
            ),
            actions=[
                TSecondaryButton(
                    label=cancel_button_label, on_click=self.on_cancel_btn_clicked
                ),
                TPrimaryButton(
                    label=proceed_button_label, on_click=self.on_proceed_btn_clicked
                ),
            ],
        )
        super().__init__(dialog=dialog, dialog_controller=dialog_controller)
        self.on_proceed_callback = on_proceed
        self.on_cancel_callback = on_cancel
        self.data_on_confirmed = data_on_confirmed

    def on_cancel_btn_clicked(self, e):
        self.close_dialog()
        if self.on_cancel_callback:
            self.on_cancel_callback()

    def on_proceed_btn_clicked(self, e):
        self.close_dialog()
        if self.data_on_confirmed is not None:
            self.on_proceed_callback(self.data_on_confirmed)
        else:
            self.on_proceed_callback()


class TPopUpMenuItem(PopupMenuItem):
    """Returns a customizable pop up menu item with standard styling"""

    def __init__(
        self,
        icon,
        txt,
        on_click,
        is_delete: bool = False,
    ):
        super().__init__(
            content=Row(
                [
                    Icon(
                        icon,
                        size=dimens.ICON_SIZE,
                        color=colors.ERROR_COLOR if is_delete else None,
                    ),
                    TBodyText(
                        txt,
                        size=fonts.BUTTON_SIZE,
                        color=colors.ERROR_COLOR if is_delete else None,
                    ),
                ]
            ),
            on_click=on_click,
        )


class TContextMenu(PopupMenuButton):
    """Returns a customizable pop up menu button with optional view, edit and delete menus"""

    def __init__(
        self,
        on_click_edit: Optional[Callable] = None,
        on_click_delete: Optional[Callable] = None,
        view_item_lbl="View Details",
        delete_item_lbl="Delete",
        edit_item_lbl="Edit",
        on_click_view: Optional[Callable] = None,
        prefix_menu_items: Optional[list[PopupMenuItem]] = None,
        suffix_menu_items: Optional[list[PopupMenuItem]] = None,
    ):

        items = []
        if prefix_menu_items:
            items.extend(prefix_menu_items)
        if on_click_view:
            items.append(
                TPopUpMenuItem(
                    icons.VISIBILITY_OUTLINED, txt=view_item_lbl, on_click=on_click_view
                ),
            )
        if on_click_edit:
            items.append(
                TPopUpMenuItem(
                    icons.EDIT_OUTLINED,
                    txt=edit_item_lbl,
                    on_click=on_click_edit,
                )
            )
        if on_click_delete:
            items.append(
                TPopUpMenuItem(
                    icons.DELETE_OUTLINE,
                    txt=delete_item_lbl,
                    on_click=on_click_delete,
                    is_delete=True,
                )
            )
        if suffix_menu_items:
            items.extend(suffix_menu_items)
        super().__init__(items=items)


class TStatusDisplay(Row):
    """Returns a text with a checked prefix icon"""

    def __init__(
        self,
        txt: str,
        is_done: bool,
    ):
        super().__init__(
            controls=[
                Icon(
                    icons.CHECK_CIRCLE_OUTLINE
                    if is_done
                    else icons.RADIO_BUTTON_UNCHECKED,
                    size=dimens.SM_ICON_SIZE,
                    color=colors.PRIMARY_COLOR if is_done else colors.GRAY_COLOR,
                ),
                TBodyText(txt),
            ]
        )


class OrView(Row):
    """Returns a view representing ---- OR ----"""

    def __init__(
        self,
        show_lines: Optional[bool] = True,
        show: bool = True,
    ):

        super().__init__(
            visible=show,
            alignment=utils.SPACE_BETWEEN_ALIGNMENT
            if show_lines
            else utils.CENTER_ALIGNMENT,
            vertical_alignment=utils.CENTER_ALIGNMENT,
            controls=[
                Container(
                    height=2,
                    bgcolor=colors.GRAY_COLOR,
                    width=100,
                    alignment=alignment.center,
                    visible=show_lines,
                ),
                TBodyText("OR", align=utils.TXT_ALIGN_CENTER, color=colors.GRAY_COLOR),
                Container(
                    height=2,
                    bgcolor=colors.GRAY_COLOR,
                    width=100,
                    alignment=alignment.center,
                    visible=show_lines,
                ),
            ],
        )


@dataclass
class NavigationMenuItem:
    """defines a menu item used in navigation rails"""

    index: int
    label: str
    icon: str
    selected_icon: str
    destination: Control
    on_new_screen_route: Optional[str] = None
    on_new_intent: Optional[str] = None


class TNavigationMenu(NavigationRail):
    """
    Returns a navigation menu for the application.

    :param title: Title of the navigation menu.
    :param on_change: Callable function to be called when the selected item in the menu changes.
    :param selected_index: The index of the selected item in the menu.
    :param destinations: List of destinations in the menu.
    :param menu_height: The height of the menu.
    :return: A NavigationRail widget containing the navigation menu.
    """

    def __init__(
        self,
        title: str,
        on_change,
        selected_index: Optional[int] = 0,
        destinations=[],
        menu_height: int = 300,
        width: int = int(dimens.MIN_WINDOW_WIDTH * 0.3),
        left_padding: int = dimens.SPACE_STD,
        top_margin: int = dimens.SPACE_STD,
    ):

        super().__init__(
            leading=Container(
                content=TSubHeading(
                    subtitle=title,
                    align=utils.TXT_ALIGN_LEFT,
                    expand=True,
                    color=colors.GRAY_DARK_COLOR,
                ),
                expand=True,
                width=width,
                margin=margin.only(top=top_margin),
                padding=padding.only(left=left_padding),
            ),
            selected_index=selected_index,
            min_width=utils.COMPACT_RAIL_WIDTH,
            extended=True,
            height=menu_height,
            min_extended_width=width,
            destinations=destinations,
            on_change=on_change,
        )


class TNavigationMenuNoLeading(Column):
    """
    Returns a navigation menu for the application without a leading content.

    :param title: Title of the navigation menu.
    :param on_change: Callable function to be called when the selected item in the menu changes.
    :param selected_index: The index of the selected item in the menu.
    :param destinations: List of destinations in the menu.
    :param menu_height: The height of the menu.
    :return: A NavigationRail widget containing the navigation menu.
    """

    def __init__(
        self,
        title: str,
        on_change,
        selected_index: Optional[int] = 0,
        destinations=[],
        menu_height: int = 200,
        width: int = int(dimens.MIN_WINDOW_WIDTH * 0.3),
        left_padding: int = dimens.SPACE_STD,
        top_margin: int = dimens.SPACE_STD,
    ):

        super().__init__()
        self.titleContainer = Container(
            content=TSubHeading(
                subtitle=title,
                align=utils.TXT_ALIGN_LEFT,
                expand=True,
                color=colors.GRAY_DARK_COLOR,
            ),
            expand=False,
            width=width,
            alignment=alignment.center_left,
            margin=margin.only(top=top_margin),
            padding=padding.only(left=left_padding),
        )
        self.navigationRail = NavigationRail(
            selected_index=selected_index,
            min_width=utils.COMPACT_RAIL_WIDTH,
            extended=True,
            height=menu_height,
            min_extended_width=width,
            destinations=destinations,
            on_change=on_change,
        )

    def setBgColor(self, side_bar_bg_color):
        # set the background color of the navigation menu
        self.navigationRail.bgcolor = side_bar_bg_color
        self.titleContainer.bgcolor = side_bar_bg_color
        # Only update if the control is mounted on the page
        if hasattr(self, "page") and self.page is not None:
            self.update()

    def build(self):
        return Column(
            controls=[
                self.titleContainer,
                self.navigationRail,
            ],
            alignment=utils.START_ALIGNMENT,
            horizontal_alignment=utils.START_ALIGNMENT,
            spacing=0,
            run_spacing=0,
        )


class TBackButton(IconButton):
    """Returns a back button"""

    def __init__(self, on_click: Optional[Callable] = None):
        return super().__init__(
            icon=icons.CHEVRON_LEFT_ROUNDED,
            on_click=on_click,
            icon_size=dimens.ICON_SIZE,
        )


class TFullScreenFormContainer(Container):
    """Returns a container for a full screen form"""

    def __init__(self, form_controls: list[Control]):
        return super().__init__(
            expand=True,
            padding=padding.all(dimens.SPACE_MD),
            margin=margin.symmetric(vertical=dimens.SPACE_MD),
            content=Card(
                expand=True,
                content=Container(
                    Column(expand=True, controls=form_controls),
                    padding=padding.all(dimens.SPACE_MD),
                    width=dimens.MIN_WINDOW_WIDTH,
                ),
            ),
        )


# ---------------------------------------------------------------------------
# Generic base classes for entity CRUD views
# ---------------------------------------------------------------------------


class EntityStates(Enum):
    """Filter states for entity lists (contracts, projects, etc.)."""

    ALL = "all"
    ACTIVE = "active"
    COMPLETED = "completed"
    UPCOMING = "upcoming"

    def __str__(self):
        return self.name.capitalize()

    @property
    def tooltip(self):
        return {
            EntityStates.ALL: "View all items",
            EntityStates.ACTIVE: "View currently active items",
            EntityStates.COMPLETED: "View completed items",
            EntityStates.UPCOMING: "View upcoming items",
        }.get(self, "")


class EntityFiltersView(Row):
    """Reusable filter buttons row for entity lists."""

    def __init__(self, on_state_changed: Callable, states_enum=EntityStates):
        super().__init__()
        self.states_enum = states_enum
        self.current_state = states_enum.ALL
        self.on_state_changed = on_state_changed
        self.filter_buttons = {}

    def on_filter_button_clicked(self, state):
        self.current_state = state
        self.set_filter_buttons()
        self.on_state_changed(state)
        self.update()

    def set_filter_buttons(self):
        for state in self.states_enum:
            self.filter_buttons[state] = ElevatedButton(
                text=str(state),
                col={"xs": 6, "sm": 3, "lg": 2},
                on_click=lambda e, s=state: self.on_filter_button_clicked(s),
                height=dimens.CLICKABLE_PILL_HEIGHT,
                color=colors.PRIMARY_COLOR
                if self.current_state == state
                else colors.GRAY_COLOR,
                tooltip=state.tooltip,
                style=ButtonStyle(
                    elevation={
                        utils.PRESSED: 3,
                        utils.SELECTED: 3,
                        utils.HOVERED: 4,
                        utils.OTHER_CONTROL_STATES: 2,
                    },
                ),
            )

    def build(self):
        self.set_filter_buttons()
        self.controls = [
            ResponsiveRow(
                controls=list(self.filter_buttons.values()),
            )
        ]


class CrudListView(TView, Column):
    """Base class for entity CRUD list views.

    Subclasses must set:
        - intent: the CrudIntent instance
        - entity_name: str (e.g. "project")
        - entity_name_plural: str (e.g. "projects")

    Subclasses must implement:
        - make_card(entity) -> Card control
        - get_card_callbacks() -> dict of callbacks for make_card (optional override)

    Optional overrides:
        - get_filters_view() -> Control or None (for filter bar)
        - on_add_intent_key -> str or None (res_utils intent key for add action)
        - open_add_editor(data) -> open inline editor for add
        - on_save_entity(entity) -> handle save result
        - load_extra_data() -> load additional data beyond entities
    """

    entity_name: str = ""
    entity_name_plural: str = ""
    on_add_intent_key: Optional[str] = None

    def __init__(self, params: TViewParams):
        TView.__init__(self, params)
        Column.__init__(self)
        self.loading_indicator = TProgressBar()
        self.no_items_control = TBodyText(
            txt=f"You have not added any {self.entity_name_plural} yet",
            color=colors.GRAY_COLOR,
            show=False,
        )
        self.title_control = ResponsiveRow(
            controls=[
                Column(
                    col={"xs": 12},
                    controls=[
                        THeading(f"My {self.entity_name_plural.title()}"),
                        self.loading_indicator,
                        self.no_items_control,
                    ],
                )
            ]
        )
        self.items_container = GridView(
            max_extent=540,
            spacing=dimens.SPACE_STD,
            run_spacing=dimens.SPACE_STD,
        )
        self.items_to_display = {}
        self.popup_handler = None

    # -- Subclass hooks --------------------------------------------------------

    def make_card(self, entity) -> Control:
        """Create a card control for the given entity. Must be overridden."""
        raise NotImplementedError

    def get_entity_description(self, entity) -> str:
        """Return a human-readable description for delete confirmation."""
        return str(entity)

    def get_filters_view(self) -> Optional[Control]:
        """Override to return a filter bar control."""
        return None

    def load_extra_data(self):
        """Override to load additional data beyond the main entity list."""
        pass

    def open_add_editor(self, data=None):
        """Override for inline add editor (contacts, clients)."""
        pass

    def on_save_entity(self, entity):
        """Override for inline save handling (contacts, clients)."""
        pass

    # -- Lifecycle methods (generic) -------------------------------------------

    def refresh_list(self):
        """Clears and rebuilds the items container from items_to_display."""
        self.items_container.controls.clear()
        for key in self.items_to_display:
            entity = self.items_to_display[key]
            card = self.make_card(entity)
            self.items_container.controls.append(card)

    def on_delete_clicked(self, entity):
        """Opens delete confirmation popup."""
        if self.popup_handler:
            self.popup_handler.close_dialog()
        desc = self.get_entity_description(entity)
        self.popup_handler = ConfirmDisplayPopUp(
            dialog_controller=self.dialog_controller,
            title="Are You Sure?",
            description=f"Are you sure you wish to delete this {self.entity_name}?\n{desc}",
            on_proceed=self.on_delete_confirmed,
            proceed_button_label="Yes! Delete",
            data_on_confirmed=entity.id,
        )
        self.popup_handler.open_dialog()

    def on_delete_confirmed(self, entity_id):
        """Deletes entity via intent, updates display."""
        self.loading_indicator.visible = True
        self.update_self()
        result = self.intent.delete(entity_id)
        is_error = not result.was_intent_successful
        msg = (
            f"{self.entity_name.title()} deleted!" if not is_error else result.error_msg
        )
        self.show_snack(msg, is_error)
        if not is_error and entity_id in self.items_to_display:
            del self.items_to_display[entity_id]
        self.refresh_list()
        self.loading_indicator.visible = False
        self.update_self()

    def on_filter_changed(self, state: EntityStates):
        """Handles filter state changes via generic intent methods."""
        if state == EntityStates.ACTIVE:
            self.items_to_display = self.intent.get_active_as_map()
        elif state == EntityStates.UPCOMING:
            self.items_to_display = self.intent.get_upcoming_as_map()
        elif state == EntityStates.COMPLETED:
            self.items_to_display = self.intent.get_completed_as_map()
        else:
            self.items_to_display = self.intent.get_all_as_map()
        self.refresh_list()
        self.update_self()

    def did_mount(self):
        self.reload_all_data()

    def parent_intent_listener(self, intent: str, data=None):
        if intent == res_utils.RELOAD_INTENT:
            self.reload_all_data()
        elif self.on_add_intent_key and intent == self.on_add_intent_key:
            self.open_add_editor(data)

    def reload_all_data(self):
        """Full reload: load entities, toggle empty message, refresh list."""
        self.mounted = True
        self.loading_indicator.visible = True
        self.update_self()
        self.load_extra_data()
        self.items_to_display = self.intent.get_all_as_map()
        count = len(self.items_to_display)
        if count == 0:
            self.no_items_control.visible = True
            self.items_container.controls.clear()
        else:
            self.no_items_control.visible = False
            self.refresh_list()
        self.loading_indicator.visible = False
        self.update_self()

    def build(self):
        filters = self.get_filters_view()
        controls = [self.title_control, Spacer(md_space=True)]
        if filters:
            controls.append(filters)
        controls.append(
            Container(
                expand=True,
                content=self.items_container,
            )
        )
        self.controls = controls

    def will_unmount(self):
        self.mounted = False
        if self.popup_handler:
            self.popup_handler.close_dialog()


class EntityDetailScreen(TView, Container):
    """Base class for entity detail/view screens.

    Subclasses must set:
        - intent: the CrudIntent instance
        - entity_name: str
        - edit_route: str (route for the editor screen)

    Subclasses must implement:
        - display_entity_data() -> populate UI controls from self.entity
        - build() -> build the UI layout
    """

    entity_name: str = ""
    edit_route: str = ""

    def __init__(self, params: TViewParams, entity_id):
        TView.__init__(self, params)
        Container.__init__(self)
        self.entity_id = entity_id
        self.loading_indicator = TProgressBar()
        self.entity = None
        self.popup_handler = None

    # -- Subclass hooks --------------------------------------------------------

    def display_entity_data(self):
        """Populate UI controls from self.entity. Must be overridden."""
        raise NotImplementedError

    # -- Generic lifecycle -----------------------------------------------------

    def did_mount(self):
        self.reload_data()

    def on_resume_after_back_pressed(self):
        self.reload_data()

    def reload_data(self):
        self.mounted = True
        self.loading_indicator.visible = True
        result = self.intent.get_by_id(self.entity_id)
        if result.was_intent_successful and result.data:
            self.entity = result.data
            self.display_entity_data()
        else:
            self.show_snack(result.error_msg, is_error=True)
        self.loading_indicator.visible = False
        self.update_self()

    def on_edit_clicked(self, e=None):
        self.navigate_to_route(self.edit_route, self.entity_id)

    def on_delete_clicked(self, e=None):
        if self.popup_handler:
            self.popup_handler.close_dialog()
        self.popup_handler = ConfirmDisplayPopUp(
            dialog_controller=self.dialog_controller,
            title="Are You Sure?",
            description=f"Are you sure you wish to delete this {self.entity_name}?",
            on_proceed=self.on_delete_confirmed,
            proceed_button_label="Yes! Delete",
            data_on_confirmed=self.entity_id,
        )
        self.popup_handler.open_dialog()

    def on_delete_confirmed(self, entity_id):
        result = self.intent.delete(entity_id)
        is_err = not result.was_intent_successful
        msg = result.error_msg if is_err else f"{self.entity_name.title()} deleted!"
        self.show_snack(msg, is_err)
        if not is_err:
            self.navigate_back()

    def on_toggle_complete_status(self, e=None):
        result = self.intent.toggle_completed(self.entity)
        if result.was_intent_successful:
            self.entity = result.data
            self.display_entity_data()
        msg = (
            result.error_msg
            if not result.was_intent_successful
            else f"{self.entity_name.title()} status updated!"
        )
        self.show_snack(msg, not result.was_intent_successful)
        self.update_self()

    def on_view_client_clicked(self, e=None):
        """Opens a popup showing the client details."""
        if not self.entity or not getattr(self.entity, "client", None):
            return
        if self.popup_handler:
            self.popup_handler.close_dialog()
        from ..clients.view import ClientViewPopUp

        self.popup_handler = ClientViewPopUp(
            dialog_controller=self.dialog_controller,
            client=self.entity.client,
        )
        self.popup_handler.open_dialog()

    def get_body_element(self, label: str, control: Control) -> ResponsiveRow:
        """Helper: returns a label + control row for detail display."""
        return ResponsiveRow(
            controls=[
                Column(
                    col={"xs": 3},
                    controls=[
                        TBodyText(
                            txt=label, weight=FontWeight.BOLD, color=colors.GRAY_COLOR
                        )
                    ],
                ),
                Column(
                    col={"xs": 9},
                    controls=[control],
                ),
            ]
        )

    def will_unmount(self):
        self.mounted = False
