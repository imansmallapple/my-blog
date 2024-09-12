import {
    ClassicEditor,
    AccessibilityHelp,
    Autoformat,
    AutoImage,
    Autosave,
    BlockQuote,
    Bold,
    CloudServices,
    Essentials,
    FontBackgroundColor,
    FontColor,
    FontFamily,
    FontSize,
    Heading,
    ImageBlock,
    ImageCaption,
    ImageInline,
    ImageInsertViaUrl,
    ImageResize,
    ImageStyle,
    ImageTextAlternative,
    ImageToolbar,
    ImageUpload,
    Indent,
    IndentBlock,
    Italic,
    Link,
    LinkImage,
    List,
    ListProperties,
    MediaEmbed,
    Paragraph,
    PasteFromOffice,
    SelectAll,
    Table,
    TableCaption,
    TableCellProperties,
    TableColumnResize,
    TableProperties,
    TableToolbar,
    TextTransformation,
    TodoList,
    Underline,
    Undo
} from 'ckeditor5';

// 自定义上传适配器
class MyUploadAdapter {
    constructor(loader) {
        this.loader = loader;
    }

    upload() {
        return this.loader.file
            .then(file => new Promise((resolve, reject) => {
                const data = new FormData();
                data.append('upload', file);

                // 向你定义的 Django 图片上传视图发起请求
                fetch('/uploads/', {
                    method: 'POST',
                    body: data,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // 获取CSRF Token
                    }
                })
                .then(response => response.json())
                .then(result => {
                    if (result && result.url) {
                        resolve({
                            default: result.url  // 返回图片URL
                        });
                    } else {
                        reject(result.error || 'Upload failed');
                    }
                })
                .catch(() => {
                    reject('Upload failed');
                });
            }));
    }

    abort() {
        // 处理取消上传的情况
    }
}

// 将自定义上传适配器绑定到编辑器
function MyCustomUploadAdapterPlugin(editor) {
    editor.plugins.get('FileRepository').createUploadAdapter = (loader) => {
        return new MyUploadAdapter(loader);
    };
}

const editorConfig = {
    toolbar: {
        items: [
            'undo',
            'redo',
            '|',
            'heading',
            '|',
            'fontSize',
            'fontFamily',
            'fontColor',
            'fontBackgroundColor',
            '|',
            'bold',
            'italic',
            'underline',
            '|',
            'link',
            'mediaEmbed',
            'imageUpload',  // 确保此项启用
            'insertTable',
            'blockQuote',
            '|',
            'bulletedList',
            'numberedList',
            'todoList',
            'outdent',
            'indent'
        ],
        shouldNotGroupWhenFull: false
    },
    plugins: [
        AccessibilityHelp,
        Autoformat,
        AutoImage,
        Autosave,
        BlockQuote,
        Bold,
        CloudServices,
        Essentials,
        FontBackgroundColor,
        FontColor,
        FontFamily,
        FontSize,
        Heading,
        ImageBlock,
        ImageCaption,
        ImageInline,
        ImageInsertViaUrl,
        ImageResize,
        ImageStyle,
        ImageTextAlternative,
        ImageToolbar,
        ImageUpload,  // 确保此项启用
        Indent,
        IndentBlock,
        Italic,
        Link,
        LinkImage,
        List,
        ListProperties,
        MediaEmbed,
        Paragraph,
        PasteFromOffice,
        SelectAll,
        Table,
        TableCaption,
        TableCellProperties,
        TableColumnResize,
        TableProperties,
        TableToolbar,
        TextTransformation,
        TodoList,
        Underline,
        Undo
    ],
    fontFamily: {
        supportAllValues: true
    },
    fontSize: {
        options: [10, 12, 14, 'default', 18, 20, 22],
        supportAllValues: true
    },
    heading: {
        options: [
            { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
            { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
            { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' },
            { model: 'heading3', view: 'h3', title: 'Heading 3', class: 'ck-heading_heading3' },
            { model: 'heading4', view: 'h4', title: 'Heading 4', class: 'ck-heading_heading4' },
            { model: 'heading5', view: 'h5', title: 'Heading 5', class: 'ck-heading_heading5' },
            { model: 'heading6', view: 'h6', title: 'Heading 6', class: 'ck-heading_heading6' }
        ]
    },
    image: {
        toolbar: [
            'toggleImageCaption',
            'imageTextAlternative',
            '|',
            'imageStyle:inline',
            'imageStyle:wrapText',
            'imageStyle:breakText',
            '|',
            'resizeImage'
        ]
    },
    link: {
        addTargetToExternalLinks: true,
        defaultProtocol: 'https://',
        decorators: {
            toggleDownloadable: {
                mode: 'manual',
                label: 'Downloadable',
                attributes: {
                    download: 'file'
                }
            }
        }
    },
    list: {
        properties: {
            styles: true,
            startIndex: true,
            reversed: true
        }
    },
    placeholder: 'Type or paste your content here!',
    table: {
        contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties']
    },
    extraPlugins: [MyCustomUploadAdapterPlugin],  // 加载自定义上传适配器插件
};

// 创建 CKEditor 实例
ClassicEditor.create(document.querySelector('#editor'), editorConfig)
    .then(editor => {
        console.log('Editor was initialized', editor);
        // 从模板获取初始数据 (这部分是 Django 模板引擎传递的数据)
        const initialData = document.querySelector('#editor').getAttribute('data-initial-data');
        console.log('initial data', initialData);
        if (initialData) {
            editor.setData(initialData);  // 如果有内容则加载到编辑器
        } else {
            editor.setData('');  // 如果没有内容，则加载空字符串
        }
        document.querySelector('#article-form').addEventListener('submit', (event) => {
            event.preventDefault();  // Prevent default form submission

            const buttonName = event.submitter ? event.submitter.name : 'add';  // Get the name of the clicked button
            const articleIdInput = document.querySelector('#article-id');
            const articleId = articleIdInput ? articleIdInput.value : '';
            const isUpdate = buttonName === 'update';
            const url = isUpdate ? `/edit_article/${articleId}/` : '/add_article/';  // Determine URL based on button

            // Debugging: Log URL and form data
            console.log('Form URL:', url);
            console.log('Article ID:', articleId);
            console.log('Button Name:', buttonName);

            // Serialize CKEditor data and send it via AJAX
            const editorData = editor.getData();
            console.log('CKEditor Data:', editorData);  // Debugging line to check editor content

            const formData = new FormData(document.querySelector('#article-form'));
            formData.append('content', editorData);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Accept': 'application/json'  // Ensure accepting JSON response
                }
            })
            .then(response => {
                console.log('Response Status:', response.status);  // Log the status of the response
                return response.json();
            })
            .then(result => {
                console.log('Server Response:', result);
                if (result.success) {
                    alert(isUpdate ? 'Article updated successfully!' : 'Article added successfully!');
                    console.log('Redirecting to:', result.redirect);  // Debugging line
                    window.location.href = result.redirect;
                } else {
                    alert(isUpdate ? 'Failed to update article' : 'Failed to add article');
                    console.error('Errors:', result.errors);  // Print errors if available
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);  // Print fetch error for debugging
                alert(isUpdate ? 'Failed to update article' : 'Failed to add article');
            });
        });

    })
    .catch(error => {
        console.error('There was a problem initializing the editor:', error);
    });
