import pandas as pd
import os
import textwrap

TESTING_DATASET_PATH = './data/human_rated_tweets.csv'
PREPROCESSED_TWEET_PATH = './data/preprocessed_twitter.csv'


def main():
    curr_ind = 0
    started_from_zero = True
    if os.path.exists(TESTING_DATASET_PATH):
        past_testing = pd.read_csv(TESTING_DATASET_PATH)
        curr_ind = len(past_testing)
        if curr_ind > 0:
            started_from_zero = False

    twitter_data = pd.read_csv(PREPROCESSED_TWEET_PATH)

    ratings = []
    print('Starting tweet rating. Please ^C to stop.\n')
    try:
        while True:
            wrapped_tweet = "\n".join(textwrap.wrap(twitter_data.iloc[curr_ind]["content"]))
            print(f'[# {curr_ind}]\nTweet: {wrapped_tweet}')
            valid_entry = False
            while not valid_entry:
                try:
                    rating = int(input('Please rate tweet between -4 (Extremely negative) to 4 (Extremely positive):\t'))
                except ValueError:
                    print('Invalid entry. Please enter a integer.')
                    continue
                if not (-4 <= rating <= 4):
                    print('Invalid entry. Please enter a integer between -4 and 4.')
                    continue
                valid_entry = True
                ratings.append(rating)
                print('\n\n')
                curr_ind += 1
    except KeyboardInterrupt:
        pass
    finally:
        if curr_ind == 0:
            exit()
        if not started_from_zero:
            prev_testing_dataset = pd.read_csv(TESTING_DATASET_PATH)
            print(f'Read last {len(prev_testing_dataset)} rated tweets memory.')
            prev_test_sentiments = prev_testing_dataset['true_sentiment']
            ratings = list(prev_test_sentiments) + ratings
        testing_dataset = twitter_data.iloc[:curr_ind]
        testing_dataset['true_sentiment'] = ratings
        print(f'Writing total of {len(testing_dataset)} rated tweets to {TESTING_DATASET_PATH}')
        testing_dataset.to_csv(TESTING_DATASET_PATH)
        print('Done.')


if __name__ == '__main__':
    main()
