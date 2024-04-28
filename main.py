import time
from functools import wraps
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Dictionary to store request counts and timestamps for each user
user_requests = {}

# Rate limiting decorator
def rate_limit(limit: int, period: int):
    def decorator(func):
        @wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            user_id = update.effective_user.id
            current_time = time.time()
            if user_id in user_requests:
                last_request_time = user_requests[user_id]["timestamp"]
                if current_time - last_request_time < period:
                    # User has exceeded the rate limit
                    update.message.reply_text("You've exceeded the rate limit. Please try again later.")
                    return
                else:
                    # Reset request count if period has passed
                    user_requests[user_id]["timestamp"] = current_time
                    user_requests[user_id]["count"] = 1
            else:
                # Initialize request count for new users
                user_requests[user_id] = {"timestamp": current_time, "count": 1}
            if user_requests[user_id]["count"] >= limit:
                # User has exceeded the rate limit
                update.message.reply_text("You've exceeded the rate limit. Please try again later.")
                return
            else:
                # Increment request count
                user_requests[user_id]["count"] += 1
            return func(update, context)
        return wrapper
    return decorator

# Function to search the website for matching URLs based on keywords
def search_website(keyword):
    # Simulated function for demonstration purposes
    # In real implementation, perform web scraping to search for URLs
    return ["https://toolzcity.com/page1", "https://toolzcity.com/page2"]

# Function to handle incoming messages
@rate_limit(limit=3, period=60)  # Limit to 3 requests per minute
def search(update: Update, context: CallbackContext):
    keyword = update.message.text.strip()
    urls = search_website(keyword)
    if urls:
        response = "Matching URLs:\n\n" + "\n".join(urls)
    else:
        response = "No matching URLs found."
    update.message.reply_text(response)

def main():
    # Set up the updater and dispatcher
    updater = Updater("7187999468:AAHCPFGGrqaq124ZBWvo1_dHIwV0WzD6Pkg", use_context=True)
    dp = updater.dispatcher

    # Add a message handler to respond to incoming messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
