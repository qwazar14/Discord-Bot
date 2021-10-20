
async def command_start(ctx, function_name):
    user = ctx.author
    return print(f'[LOG] {user} called command "{function_name}"')


async def command_done(function_name):
    return print(f'[LOG] {function_name} command done!')
