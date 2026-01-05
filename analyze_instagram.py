import os
import re

def extract_users_from_html(file_path):
    """Extracts usernames from an Instagram HTML file using regex."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return set()

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match: href="https://www.instagram.com/_u/USERNAME" OR href="https://www.instagram.com/USERNAME"
    pattern = r'href="https://www.instagram.com/(?:_u/)?([^"]+)"'
    users = re.findall(pattern, content)
    return set(users)

def write_list_to_file(filename, title, users):
    """Writes a list of users to a numbered text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{title} ({len(users)}):\n")
        for idx, user in enumerate(sorted(list(users)), 1):
            f.write(f"{idx}. {user}\n")
    print(f"Generated {filename}")

def main():
    # Input files
    following_html = 'connections/followers_and_following/following.html'
    followers_html = 'connections/followers_and_following/followers_1.html'

    # Extract users
    print("Extracting users from HTML files...")
    following_set = extract_users_from_html(following_html)
    followers_set = extract_users_from_html(followers_html)

    if not following_set or not followers_set:
        print("Error: Could not extract users. Make sure HTML files exist.")
        return

    print(f"Found {len(following_set)} users in Following.")
    print(f"Found {len(followers_set)} users in Followers.")

    # Calculate categories
    fans = followers_set - following_set
    not_following_back = following_set - followers_set

    # Define output files
    outputs = [
        ("followers.txt", "FOLLOWERS (Todos los que me siguen)", followers_set),
        ("following.txt", "FOLLOWING (Todos los que sigo)", following_set),
        ("me_siguen_no_sigo.txt", "QUE ME SIGUE Y NO SIGO (Fans)", fans),
        ("sigo_no_me_siguen.txt", "QUE SIGO Y NO ME SIGUE (No me devuelven el follow)", not_following_back)
    ]

    # Generate files
    for filename, title, user_set in outputs:
        write_list_to_file(filename, title, user_set)

    # Optional: cleanup intermediate txt files if they exist from previous runs
    files_to_remove = [
        'followers_users.txt', 'followers_users_enumerated.txt',
        'following_users.txt', 'following_users_enumerated.txt',
        'comparison_results.txt', 'reporte_usuarios.txt',
        '1_followers.txt', '2_following.txt', 
        '3_me_siguen_no_sigo.txt', '4_sigo_no_me_siguen.txt'
    ]
    
    deleted_count = 0
    for f in files_to_remove:
        if os.path.exists(f):
            os.remove(f)
            deleted_count += 1
    
    if deleted_count > 0:
        print(f"Cleaned up {deleted_count} old files.")

if __name__ == "__main__":
    main()
