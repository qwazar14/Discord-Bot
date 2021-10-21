async def command_start(ctx):
    user = ctx.author
    command_name = ctx.command
    print(f'[LOG] {user} called command "{command_name}"')


async def command_done(ctx):
    command_name = ctx.command
    print(f'[LOG] "{command_name}" command done!')
