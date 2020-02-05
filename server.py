from http.server import BaseHTTPRequestHandler, HTTPServer

from sun import Sun
from leds import LEDS

light = LEDS(brightness = 0.5)

class HueRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            path_split = self.path.split('?')

            if (len(path_split) > 1) and (path_split[0] == '/LEDS'):
                specifiers = path_split[1].split('+')

                for specifier in specifiers:
                    key, value = specifier.split('=')
                    if key == 'on':
                        brightness = 0.5 if value == 'true' else 0.0
                        light.set_brightness(brightness)
                    elif key == 'brightness':
                        brightness = float(value)
                        light.set_brightness(brightness)
                    elif key == 'temperature':
                        temperature = float(value)
                        r, g, b = Sun.kelvin_to_rgb(temperature)
                        light.fill(r, g, b)
                    elif key == 'duotone':
                        r1, g1, b1, r2, g2, b2, seg = value.split(',')
                        light.duotone((r1, g1, b1), (r2, g2, b2), int(seg))
                    elif key == 'r':
                        light.set_r(float(value))
                    elif key == 'g':
                        light.set_g(float(value))
                    elif key == 'b':
                        light.set_b(float(value))

            print(self.path)
            self.send_http()

        except BrokenPipeError: pass

    def create_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html>
            <head>
                <title>Title goes here.</title>
                </head>
            <body>
                <p>This is a test.</p>
                <p>You accessed path: {}</p>
            </body>
        </html>
        '''.format(path)
        return bytes(content, 'UTF-8')

    def send_http(self):
        http = self.create_http(200, self.path)
        self.wfile.write(http)

if __name__ == '__main__':
    import os.path
    if os.path.exists('serving.txt'):
        exit()

    open('serving', 'a').close()

    server = HTTPServer(('127.0.0.1', 8080), HueRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    LEDS.deinit()

    import os
    os.remove('serving.txt')
