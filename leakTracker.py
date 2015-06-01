import praw
import smtplib

redditUsername = ""
redditPassword = ""
emailUsername = ""
emailPassword = ""
#Use SMS gateways (e.g. phonenumber@carriergateway.com)
phoneNum = [""]


def setupReddit(username, password):
    r = praw.Reddit("LeakTracker v1.0 by /u/freshaaron")
    r.login(username, password)
    return r


def writeToSet(id):
    with open("checkedAlbums.txt", "a+") as f:
        f.write("{id}\n".format(id=submission.id))


def generateSet():
    with open("checkedAlbums.txt") as f:
        already_done = [x.strip("\n") for x in f.readlines()]
        return already_done


def sendEmail(username, password, phonenum):
    email = smtplib.SMTP("smtp.gmail.com", 587)
    email.ehlo()
    email.starttls()
    email.login(username, password)
    email.sendmail("New Leak", phonenum, "{album} has leaked!".format(
        album=submission.title))
    email.quit()
    print("Email Sent to {num}: {album} has leaked!".format(
        num=phonenum, album=submission.title))

if __name__ == "__main__":
    r = setupReddit(redditUsername, redditPassword)
    print("[LeakTracker] Logged into Reddit.")
    try:
        already_done = generateSet()
        print("[LeakTracker] Generating previous IDs from checkedAlbums.txt")
    except (OSError, IOError):
        already_done = []
        print(("[LeakTracker] checkedAlbums.txt not found"
              ", generating empty list."))
    while True:
        for submission in r.get_subreddit("leakthreads").get_new():
            if(submission.id not in already_done):
                for number in phoneNum:
                    sendEmail(emailUsername, emailPassword, number)
                writeToSet(submission.id)
                print(("[LeakTracker] {title} (#{id}) has been added"
                      "to checkedAlbums.txt").format(
                    title=submission.title, id=submission.id))
                already_done = generateSet()

