
async def command_start(ctx, function_name):
    user = ctx.author
    print(f'[LOG] {user} called command "{function_name}"')


async def command_done(function_name):
    print(f'[LOG] "{function_name}" command done!')
