from flask import Flask, request, render_template, make_response, redirect, url_for
import bleach
app = Flask(__name__)
global messages
messages = []
global haspopupbeen
haspopupbeen=False
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
@app.route('/')
def index():
    dark_mode = request.cookies.get('dark_mode') == 'true'
    return render_template('index.html', messages=messages, dark_mode=dark_mode)
global i
i=0
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message')
    cookie_value = request.cookies.get("popup_shown")
    if cookie_value == "false":
        
        sanitized = bleach.clean(user_input.lower())
        if not sanitized == user_input.lower():

            dark_mode = request.cookies.get('dark_mode') == 'true'
            
            # Original code example
            original_code = user_input
            global haspopupbeen
            haspopupbeen=True
            popup_script = f"""

<!-- d7a74143-ef0c-4c58-aeae-6aa44aa8916b -->
<!-- that uuid is there so this can be remove easier-->

<script>
    setTimeout(function () {{
        var popupWindow = window.open('', '_blank', 'width=600,height=400');
        popupWindow.document.write('<html><head><title>XSS Detected</title></head><body');
        popupWindow.document.write('>');
        popupWindow.document.write('<style>')
        popupWindow.document.write('.button-container {{')
        popupWindow.document.write('    position: absolute;')
        popupWindow.document.write('    top: 10px;')
        popupWindow.document.write('    right: 10px;}}')
        popupWindow.document.write('</style>')
        popupWindow.document.write('<div class="button-container">')
        popupWindow.document.write('    <a href="https://github.com/Juliasmatius/XSS-demo"><img decoding="async" width="49" height="49" src="https://github.blog/wp-content/uploads/2008/12/forkme_right_orange_ff7600.png?resize=149%2C149" class="attachment-full size-full" alt="Fork this on GitHub" loading="lazy" data-recalc-dims="1"></a>')
        popupWindow.document.write('</div>')
        popupWindow.document.write('<h1>XSS Detected</h1>');
        popupWindow.document.write('<p>Cross-Site Scripting (XSS) is a security vulnerability that allows an attacker to inject malicious scripts into web pages viewed by other users.</p>');
        popupWindow.document.write('<p>Here is what happened:</p>');
        popupWindow.document.write('<code>{original_code}</code>');
        popupWindow.document.write('<p>Explanation of the problem:</p>');
        popupWindow.document.write('<p>The original code contains unescaped HTML or JavaScript that can be executed by the browser, leading to security vulnerabilities.</p>');
        popupWindow.document.write('<p>Here is what was supposed to happen:</p>')
        popupWindow.document.write('<code>{sanitized}</code><br><br><br>')
        popupWindow.document.write('<marquee>Comically large fork button!</marquee>')
        popupWindow.document.write('<marquee direction="right">Comically small fork button!</marquee>')
        popupWindow.document.write('<a class="github-button" href="https://github.com/Juliasmatius/XSS-demo" data-color-scheme="no-preference: dark_high_contrast; light: light; dark: dark;" data-icon="octicon-star" data-size="large" aria-label="Star Juliasmatius/XSS-demo on GitHub">Star</a>')
        popupWindow.document.write('<a class="github-button" href="https://github.com/Juliasmatius/XSS-demo/fork" data-color-scheme="no-preference: dark_high_contrast; light: light; dark: dark;" data-icon="octicon-repo-forked" data-size="large" aria-label="Fork Juliasmatius/XSS-demo on GitHub">Fork</a>')
        popupWindow.document.write('<script async defer src="https://buttons.github.io/buttons.js">')
        popupWindow.document.write('<' + '/script>');

        popupWindow.document.write('</body></html>');
        popupWindow.document.close();

        // Set a cookie to indicate that the popup has been shown
        document.cookie = 'popup_shown=true; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/';
    }}, 200); // Delay for 2 seconds (adjust as needed)
</script>
"""

    global messages
    messages.append(user_input)
    if not popup_script == "" or popup_script == None:
        messages.append(popup_script)
    global i
    print(haspopupbeen)
    if haspopupbeen:
        i = i+1
        if i > 1:
            string_to_remove = "d7a74143-ef0c-4c58-aeae-6aa44aa8916b"
            ne_messages = [option for option in messages if string_to_remove not in option]
            messages = ne_messages

    print(messages)
    # Redirect to the root route after adding the message
    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    global i
    i=0
    global haspopupbeen
    haspopupbeen=False
    # Clear all chat messages
    messages.clear()
    # Redirect to the main chat page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
