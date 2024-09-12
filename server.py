from aiohttp import web
import pathlib

async def handle_components(request):
    filename = request.match_info['filename']
    file_path = pathlib.Path(__file__).parent / 'components' / filename
    if file_path.is_file():
        return web.FileResponse(file_path)
    else:
        return web.Response(status=404, text='File not found')


app = web.Application()
app.router.add_route('GET', '/components/{filename}', handle_components)
app.router.add_static('/', 'C:\Project skeleton\static', name='static')


if __name__ == '__main__':
    web.run_app(app, port=8080)
