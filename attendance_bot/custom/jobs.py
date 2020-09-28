from attendance_bot import dispatcher


def _delete_message(ctx):
    data = ctx.job.context
    dispatcher.bot.delete_message(data[0], data[1])


def schedule_delete(chat_id, message_id, time):
    return dispatcher.job_queue.run_once(
        _delete_message, time, context=[chat_id, message_id]
    )
