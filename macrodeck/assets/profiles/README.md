# MacroDeck - assets - profiles
These are the bundled profiles for MacroDeck as well as `empty-profile.json`, an example profile / template.


## Profile Structure
MacroDeck profiles are JSON files that describe both deck attributes, as well as a list of windows and the keymap which to use when that window is focused.

### Example
Here is a simple example of a profile that executes a keyboard shortcut if any `lxterminal` window is focused.

```json
{
	"name": "simple-profile",
	"description": "A simple example MacroDeck profile",
	"enabled": true,

	"deck": {
		"brightness": 1.0
	},

	"windows": [
		{
			"title": "*lxterminal*",
			"keys": [
				{
					"name": "new-tab",
					"icon": "add/to/queue",
					"actions": [
						{
							"type": "keystoke",
							"payload": "<Ctrl>+T"
						}
					]
				}
			]
		}
	]
}
```

The first few elements are self-explanatory.
```json
"name": "simple-profile",
"description": "A simple example MacroDeck profile",
"enabled": true,
```

We have `name`, `description`, and `enabled`, these describe the profile metadata.

Next we have the active deck attributes, in this case only the brightness is set.

After that we have the collection of windows we wish to match against in the profile, for this example, we only have one. Inside the window, we have the `title` attribute with is a regex for the window title you'd like to match, as well as the collection of keys you wish to setup.

Each key will be added to the active deck in order, currently only up to the maximum number of keys supported by the deck will be rendered, however key pagination is planned for a future release.

In the one key we wish to add, we have the name of the key, as well as it's icon. The icon is a relative path name for the image you wish to show, this is used in conjunction with `icon_styles` described later in this document. You may specify a full, absolute path to an arbitrary image to use as an icon as well, however you must then set the `icon_absolute` attribute to `true` for the key.

We then have the list of actions we wish for the key to execute once pressed. You may have as many actions as you wish per key.

The single action we have for this key is a `keystroke` action, this will execute a key-combination in the target window. Modifier keys are between `<` and `>` and the `+` operator is used to join keys together. For more details on the various possible actions see the Actions section in this document.

This profile can then be loaded into MacroDeck by either placing it in the `assets/profiles` directory, in the install location, or in the `.config/macrodeck/profiles` directory in your home directory. 


### Profile Metadata
The profile can contain the following metadata fields in addition to the required `deck`, and `windows` fields and the optional `icon_styles` field.

 * `name` - The name of the profile (required)
 * `description` - The description of the profile (optional)
 * `enabled` - If the profile is enabled or not (optional, defaults to true)


### Deck Attributes
The `deck` field can contain the following attributes.

 * `brightness` - The brightness to set the deck screens to (optional, defaults to 1.0)
 * `serial` - The deck serial number (optional)

#### Brightness
You can specify the deck brightness as a value between `0.0` and `1.0` for fully dim or fully bright.

#### Serial
You can specify the deck serial number, the profile will only be loaded if the serial number of the active deck matches this.

### Icon Styles
You can specify various details about the built-in icons that are used for the key images in the `icon_styles` field.

 * `dpi` - The DPI of the icon (optional, defaults to '48')
 * `colour` - The colour of the icon (optional, defaults to 'white')
 * `type` - The file extension of the icon (optional, defaults to 'png')

These are used by MacroDeck internally to produce the full path to the icon for each key.

For example, with the default settings, an icon with the name `open/with` will be resolved to the path `ASSET_DIR/icons/open/with/white/48dp.png` where `ASSET_DIR` is the absolute path to the installed asset locations

All of these settings are specific to how MacroDeck uses the Matrial Design icons in the icons director.

#### DPI
The DPI of the icon, it can be any one of the following values and defaults to `48`.

 * 18
 * 24
 * 36
 * 48

#### Colour
The foreground colour of the icon, it can be any one of the following values and defaults to `white`.

 * white
 * black

#### Type
The file extension of the icon, currently only `png` is used and as such it is also the default.

### Windows
You can specify any number of window objects to match on. Each one must have at least a `title` field, and zero or more `key` objects. They can contain the following fields.

 * `title` - The title of the window to match on (required)
 * `keys` - The collection of key objects to match on (optional)

#### Title
The title of the window to match on for the contextual macros. This field supports regular expressions for matching.

### Keys
You can specify zero or more `key` objects per window object, they can contain any number of actions and must have a `name` field. They support the following fields.

 * `name` - The name of they key (required)
 * `text` - Text to be rendered on the key (optional)
 * `icon` - The icon name for the key (optional)
 * `icon_pressed` - The icon name for the icon the key will show in the held state (optional)
 * `icon_absolute` - Specifies if the icon name is an absolute path to an image file for both `icon` and `icon_pressed` (optional, defaults to false)
 * `actions` - The collection of zero or more `action` objects to execute on a key event

### Actions
You can specify zero or more `action` objects to execute when a key event happens. It must have a `type` and a `payload`. They support the following fields.

 * `on` - The event to trigger on (optional, defaults to 'pressed')
 * `type` - The type of event to trigger on (required)
 * `payload` - The payload to execute when the action is triggered (required)


The `payload` is contextual to `type` as described below.

#### On
The event type to trigger the action on, it can be one of the following values and defaults to `pressed`

 * pressed
 * released


#### Type
The type of action this is going to execute, it can be one of the following values.

 * `text` - Type text as a user would
 * `keystroke` - Send a keystroke
 * `exec` - Execute a program


For actions typed `text`, `payload` is a simple text string with support for `\n`, `\t`, `\'`, `\"`, and `\\`. An example of an action using this type is as follows.

```json
"type": "text",
"payload": "I am a string with \"quotation\" marks and a \n newline."
```

For actions typed `keystroke`, `payload` is either a single string with a keystroke specifier, or a list of keystrokes to press in order. This payload supports sending arbitrary scan codes to the focused window as well.

Modifier keys are surrounded with `<` and `>`, and raw scan codes are sent with `\xHH` to specify a raw hex scan code to send. Key strokes are joined with the `+` operator and support up to 4 held keys.

The following modifiers are named for this payload.

 * `<Ctrl>`   - The left-hand control key
 * `<LCtl>`   - The same as `<Ctrl>`
 * `<RCtl>`   - The right-hand control key
 * `<Alt>`    - The left-hand alt key
 * `<LAlt>`   - The same as `<Alt>`
 * `<RAlt>`   - The Right-hand alt key
 * `<Shift>`  - The left-hand shift key
 * `<LShift>` - The same as `<Shift>`
 * `<RShift>` - The right-hand shift key
 * `<Super>`  - The left-hand super key
 * `<RSuper>` - The same as `<Super>`
 * `<LSuper>` - The right-hand super key
 * `<CpsLck>` - The caps-lock key.

More keys are planned to have actual names, but in the mean time if you don't see a modifier key you need, then you can specify it with a series of hex escapes. For example, if you with to send a `henkan/zenkouho` to the focused window then you'd use `\x79` in the shortcut. Multi-byte scan codes are also supported, just chain multiple escapes together without a joiner.
