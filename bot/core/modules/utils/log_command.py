async def command_start(ctx):
    user = ctx.author
    command_name = ctx.command
    print(f'[INFO] {user} called command "{command_name}"')


async def command_done(function_name):
    return print(f'[INFO] {function_name} command done!')
