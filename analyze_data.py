#!/usr/bin/env python3
"""
Analyze MyBambu 2025 Social Media Data
Extracts key metrics for the highlights report
"""

import csv
import json
from datetime import datetime

def analyze_account_metrics(csv_path):
    """Analyze the main account metrics CSV"""

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Get first and last rows for follower growth
    first_row = rows[0]
    last_row = rows[-1]

    # Extract follower counts (from the aggregated followers column)
    followers_col = "Followers (This column might contain aggregated values across networks. To see the breakdown, head into Hootsuite and use compare by social network. You can customize these metric tiles in Hootsuite to see how each network contributed to the total. Overall aggregated value for Social Networks: MyBambu, MyBambu, mybambu.us, mybambu, MyBambu, @mybambu_us)"

    start_followers = float(first_row[followers_col]) if first_row[followers_col] else 0
    end_followers = float(last_row[followers_col]) if last_row[followers_col] else 0
    follower_growth = end_followers - start_followers

    # Get platform-specific follower data from last row
    fb_followers = float(last_row["Followers > Social network - Facebook Page (Daily aggregated values for Social Networks: mybambu.us, @mybambu_us, MyBambu, mybambu, MyBambu, MyBambu)"]) if last_row["Followers > Social network - Facebook Page (Daily aggregated values for Social Networks: mybambu.us, @mybambu_us, MyBambu, mybambu, MyBambu, MyBambu)"] else 0
    ig_followers = float(last_row["Followers > Social network - Instagram Business (Daily aggregated values for Social Networks: mybambu.us, @mybambu_us, MyBambu, mybambu, MyBambu, MyBambu)"]) if last_row["Followers > Social network - Instagram Business (Daily aggregated values for Social Networks: mybambu.us, @mybambu_us, MyBambu, mybambu, MyBambu, MyBambu)"] else 0
    tiktok_followers = float(last_row["Followers > Social network - TikTok Business (Daily aggregated values for Social Networks: mybambu.us, @mybambu_us, MyBambu, mybambu, MyBambu, MyBambu)"]) if last_row["Followers > Social network - TikTok Business (Daily aggregated values for Social Networks: mybambu.us, @mybambu_us, MyBambu, mybambu, MyBambu, MyBambu)"] else 0

    # Sum up total reactions, impressions, video views across all rows
    reactions_col = "Post reactions & likes (This column might contain aggregated values across networks. To see the breakdown, head into Hootsuite and use compare by social network. You can customize these metric tiles in Hootsuite to see how each network contributed to the total. Overall aggregated value for Social Networks: MyBambu, MyBambu, mybambu, @mybambu_us, mybambu.us, MyBambu)"
    impressions_col = "Post impressions (This column might contain aggregated values across networks. To see the breakdown, head into Hootsuite and use compare by social network. You can customize these metric tiles in Hootsuite to see how each network contributed to the total. Overall aggregated value for Social Networks: MyBambu, mybambu.us, MyBambu, @mybambu_us, MyBambu, mybambu)"
    video_views_col = "Post video views (This column might contain aggregated values across networks. To see the breakdown, head into Hootsuite and use compare by social network. You can customize these metric tiles in Hootsuite to see how each network contributed to the total. Overall aggregated value for Social Networks: @mybambu_us, mybambu, MyBambu, MyBambu, MyBambu)"
    comments_col = "Post comments & replies (This column might contain aggregated values across networks. To see the breakdown, head into Hootsuite and use compare by social network. You can customize these metric tiles in Hootsuite to see how each network contributed to the total. Overall aggregated value for Social Networks: MyBambu, mybambu.us, MyBambu, MyBambu, mybambu, @mybambu_us)"
    shares_col = "Post shares (This column might contain aggregated values across networks. To see the breakdown, head into Hootsuite and use compare by social network. You can customize these metric tiles in Hootsuite to see how each network contributed to the total. Overall aggregated value for Social Networks: mybambu, MyBambu, @mybambu_us, MyBambu, MyBambu, mybambu.us)"
    posts_col = "Posts (This column might contain aggregated values across networks. To see the breakdown, head into Hootsuite and use compare by social network. You can customize these metric tiles in Hootsuite to see how each network contributed to the total. Overall aggregated value for Social Networks: MyBambu, MyBambu, mybambu, MyBambu, mybambu.us, @mybambu_us)"

    total_reactions = 0
    total_impressions = 0
    total_video_views = 0
    total_comments = 0
    total_shares = 0
    total_posts = 0

    # Platform-specific metrics
    fb_impressions = 0
    ig_impressions = 0
    tiktok_impressions = 0

    fb_reactions = 0
    ig_reactions = 0
    tiktok_reactions = 0

    for row in rows:
        # Total metrics
        if row[reactions_col]:
            total_reactions += float(row[reactions_col])
        if row[impressions_col]:
            total_impressions += float(row[impressions_col])
        if row[video_views_col]:
            total_video_views += float(row[video_views_col])
        if row[comments_col]:
            total_comments += float(row[comments_col])
        if row[shares_col]:
            total_shares += float(row[shares_col])
        if row[posts_col]:
            total_posts += float(row[posts_col])

        # Platform-specific impressions
        fb_imp_col = "Post impressions - Facebook Page (Daily aggregated values for Social Networks: MyBambu, @mybambu_us, MyBambu, mybambu, MyBambu, mybambu.us)"
        ig_imp_col = "Post impressions - Instagram Business (Daily aggregated values for Social Networks: MyBambu, @mybambu_us, MyBambu, mybambu, MyBambu, mybambu.us)"
        tiktok_imp_col = "Post impressions - TikTok Business (Daily aggregated values for Social Networks: MyBambu, @mybambu_us, MyBambu, mybambu, MyBambu, mybambu.us)"

        if row[fb_imp_col]:
            fb_impressions += float(row[fb_imp_col])
        if row[ig_imp_col]:
            ig_impressions += float(row[ig_imp_col])
        if row[tiktok_imp_col]:
            tiktok_impressions += float(row[tiktok_imp_col])

        # Platform-specific reactions
        fb_react_col = "Post reactions & likes - Facebook Page (Daily aggregated values for Social Networks: @mybambu_us, mybambu.us, mybambu, MyBambu, MyBambu, MyBambu)"
        ig_react_col = "Post reactions & likes - Instagram Business (Daily aggregated values for Social Networks: @mybambu_us, mybambu.us, mybambu, MyBambu, MyBambu, MyBambu)"
        tiktok_react_col = "Post reactions & likes - TikTok Business (Daily aggregated values for Social Networks: @mybambu_us, mybambu.us, mybambu, MyBambu, MyBambu, MyBambu)"

        if row[fb_react_col]:
            fb_reactions += float(row[fb_react_col])
        if row[ig_react_col]:
            ig_reactions += float(row[ig_react_col])
        if row[tiktok_react_col]:
            tiktok_reactions += float(row[tiktok_react_col])

    # Calculate total engagement
    total_engagement = total_reactions + total_comments + total_shares

    # Calculate engagement rate
    engagement_rate = (total_engagement / total_impressions * 100) if total_impressions > 0 else 0

    return {
        "start_followers": int(start_followers),
        "end_followers": int(end_followers),
        "follower_growth": int(follower_growth),
        "follower_growth_pct": (follower_growth / start_followers * 100) if start_followers > 0 else 0,
        "total_reactions": int(total_reactions),
        "total_impressions": int(total_impressions),
        "total_video_views": int(total_video_views),
        "total_comments": int(total_comments),
        "total_shares": int(total_shares),
        "total_engagement": int(total_engagement),
        "total_posts": int(total_posts),
        "engagement_rate": round(engagement_rate, 2),
        "platforms": {
            "facebook": {
                "followers": int(fb_followers),
                "impressions": int(fb_impressions),
                "reactions": int(fb_reactions)
            },
            "instagram": {
                "followers": int(ig_followers),
                "impressions": int(ig_impressions),
                "reactions": int(ig_reactions)
            },
            "tiktok": {
                "followers": int(tiktok_followers),
                "impressions": int(tiktok_impressions),
                "reactions": int(tiktok_reactions)
            }
        }
    }

def main():
    csv_path = "/Users/paulahernandez/Downloads/social_media_data/year_in_review_2025_2025-01-01_to_2025-12-31_created_on_20251216T1737Z_account_metrics.csv"

    metrics = analyze_account_metrics(csv_path)

    # Save to JSON
    with open('/Users/paulahernandez/mybambu-social-highlights-2025/metrics.json', 'w') as f:
        json.dump(metrics, indent=2, fp=f)

    # Print summary
    print("=== MyBambu 2025 Social Media Metrics ===\n")
    print(f"Total Followers (Dec 31): {metrics['end_followers']:,}")
    print(f"Follower Growth: +{metrics['follower_growth']:,} ({metrics['follower_growth_pct']:.1f}%)")
    print(f"\nTotal Impressions: {metrics['total_impressions']:,}")
    print(f"Total Reactions/Likes: {metrics['total_reactions']:,}")
    print(f"Total Comments: {metrics['total_comments']:,}")
    print(f"Total Shares: {metrics['total_shares']:,}")
    print(f"Total Engagement: {metrics['total_engagement']:,}")
    print(f"Engagement Rate: {metrics['engagement_rate']}%")
    print(f"Total Video Views: {metrics['total_video_views']:,}")
    print(f"Total Posts: {metrics['total_posts']:,}")
    print(f"\n--- Platform Breakdown ---")
    print(f"\nFacebook:")
    print(f"  Followers: {metrics['platforms']['facebook']['followers']:,}")
    print(f"  Impressions: {metrics['platforms']['facebook']['impressions']:,}")
    print(f"  Reactions: {metrics['platforms']['facebook']['reactions']:,}")
    print(f"\nInstagram:")
    print(f"  Followers: {metrics['platforms']['instagram']['followers']:,}")
    print(f"  Impressions: {metrics['platforms']['instagram']['impressions']:,}")
    print(f"  Reactions: {metrics['platforms']['instagram']['reactions']:,}")
    print(f"\nTikTok:")
    print(f"  Followers: {metrics['platforms']['tiktok']['followers']:,}")
    print(f"  Impressions: {metrics['platforms']['tiktok']['impressions']:,}")
    print(f"  Reactions: {metrics['platforms']['tiktok']['reactions']:,}")

if __name__ == "__main__":
    main()
