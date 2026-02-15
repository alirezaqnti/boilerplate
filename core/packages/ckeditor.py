CKEDITOR_5_CONFIGS = {
    "default": {
        "menubar": True,
        "toolbar": {
            "items": [
                "heading",
                "style",
                "|",
                "bold",
                "italic",
                "underline",
                "strikethrough",
                "fontSize",
                "fontFamily",
                "fontColor",
                "fontBackgroundColor",
                "|",
                "alignment",
                "|",
                "bulletedList",
                "numberedList",
                "todoList",
                "|",
                "outdent",
                "indent",
                "|",
                "link",
                "blockQuote",
                "code",
                "codeBlock",
                "|",
                "insertTable",
                "imageUpload",
                "mediaEmbed",
                "|",
                "undo",
                "redo",
                "|",
                "removeFormat",
                "sourceEditing",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph"},
                {"model": "heading1", "view": "h1", "title": "Heading 1"},
                {"model": "heading2", "view": "h2", "title": "Heading 2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3"},
                {"model": "heading4", "view": "h4", "title": "Heading 4"},
            ]
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:inline",
                "imageStyle:block",
                "imageStyle:alignLeft",
                "imageStyle:alignCenter",
                "imageStyle:alignRight",
                "|",
                "resizeImage",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "codeBlock": {
            "languages": [
                {"language": "plaintext", "label": "Plain text"},
                {"language": "python", "label": "Python"},
                {"language": "javascript", "label": "JavaScript"},
                {"language": "html", "label": "HTML"},
                {"language": "css", "label": "CSS"},
                {"language": "json", "label": "JSON"},
                {"language": "bash", "label": "Bash"},
            ]
        },
        "mediaEmbed": {
            "previewsInData": True,
        },
        "mention": {
            "feeds": [
                {
                    "marker": "{",
                    "minimumCharacters": 0,
                    "feed": [
                        "{{first_name}}",
                        "{{last_name}}",
                        "{{company_name}}",
                        "{{contract_date}}",
                        "{{signature}}",
                    ],
                }
            ]
        },
        "htmlSupport": {
            "allow": [
                {
                    "name": r".*",
                    "attributes": True,
                    "classes": True,
                    "styles": True,
                }
            ]
        },
    }
}


customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]
