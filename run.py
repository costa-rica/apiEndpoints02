from flask import Flask, render_template, redirect, url_for, request, abort, \
    jsonify, send_from_directory
import os
import time
from tr01_models import sess, Users, Rincons, RinconsPosts, UsersToRincons, \
    RinconsPostsComments, RinconsPostsLikes, RinconsPostsCommentsLikes
from utils import create_rincon_posts_list, \
    create_rincon_posts_list_new, create_rincon_post_dict
from tr01_config import ConfigLocal

app = Flask(__name__)


# SITE_KEY = '6LfSSbckAAAAAA6pMVYzEAXdZW5Bq59BTEVMCZn5'
SECRET_KEY = '6LfSSbckAAAAAIE8NiOuh4Cr0WqaPXJqz2LkmUpO'
# VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
config = ConfigLocal()


@app.route("/", methods=['GET','POST'])
def home():

    print("Looks good")

    return jsonify({"message":"from home page"})

@app.route("/are_we_running", methods=["GET"])
def are_we_runnnig():

    print("Looks good")

    return jsonify({"message":"Tout ça marché bien!"})

@app.route("/call_for_image/<image_filename>", methods=['GET','POST'])
def call_for_image(image_filename):

    dir_path = '/Users/nick/Documents/_databases/tr01/rincon_files/1_costa_rica'

    print(f"- /call_for_image respose with filename sent: {image_filename}") 

    if os.environ.get('FLASK_ENV')=='local':
        print("*** sleeping for 5 seconds *")
        time.sleep(5)


    return send_from_directory(dir_path, image_filename)


@app.route("/rincon_posts/<rincon_id>", methods=["POST"])
def rincon(rincon_id):

    print(f"- accessed rincon endpoint with rincon_id: {rincon_id}")
    
    rincon = sess.query(Rincons).filter_by(id= rincon_id).first()


    posts_list = create_rincon_posts_list(1, rincon_id, True)

    print(f"- sending rincon's post: {len(posts_list)} posts")
    print(f"- first post is: {posts_list[0]}")

    return jsonify(posts_list)

# New def rincon(rincon_id)
@app.route("/get_rincon_posts_new/", methods=["POST"])
def get_rincon_posts_new():

    # print(f"- accessed rincon endpoint with rincon_id: {rincon_id}")
    current_user = sess.get(Users,1)
    
    try:
        request_json = request.json
        print("request_json:",request_json)
        rincon_id = request_json.get("id")
    except Exception as e:
        print(e)
        return make_response('Could not verify', 400, {'message' : 'httpBody data recieved not json not parse-able.'})

    rincon = sess.query(Rincons).filter_by(id= rincon_id).first()
    posts_list = create_rincon_posts_list_new(current_user, rincon_id)

    if len(posts_list) == 0:
        print("add a post")
        posts_list = create_empty_rincon_post_dict(current_user,rincon_id )
    # print("----------")
    # print(posts_list)
    # print("-----------")
    return jsonify(posts_list)



# New def get photo
@app.route("/get_rincon_image", methods=["POST"])
def get_rincon_image( ):
    print("- in get_rincon_image")
    current_user = sess.get(Users, 1)
    try:
        request_json = request.json
        print("request_json:",request_json)
        rincon = sess.query(Rincons).filter_by(id = request_json["id"]).first()
        rincon_files_db_folder_name = f"{rincon.id}_{rincon.name_no_spaces}"
    except Exception as e:
        print("FAiled to decode json: ", e)
        return jsonify({"status": "httpBody data recieved not json not parse-able."})

    file_name = request_json.get('image_filename')

    if len(file_name.split(",")) > 0:
        file_list = file_name.split(",")
        image_filename = file_list[0]
    else:
        image_filename = file_name

    time.sleep(3)

    print("File location: ")
    print(os.path.join(config.DB_ROOT,"rincon_files", rincon_files_db_folder_name))

    return send_from_directory(os.path.join(config.DB_ROOT,"rincon_files", \
        rincon_files_db_folder_name), image_filename)

# Old get photo endpoint
@app.route("/rincon_post_file/<file_name>", methods=["POST"])
def rincon_file( file_name):
    print("*** calling for images ***")
    current_user = sess.get(Users, 1)
    try:
        request_json = request.json
        print("request_json:",request_json)
        rincon = sess.query(Rincons).filter_by(id = request_json["rincon_id"]).first()
        rincon_files_db_folder_name = f"{rincon.id}_{rincon.name_no_spaces}"
    except Exception as e:
        logger_main.info(e)
        return jsonify({"status": "httpBody data recieved not json not parse-able."})


    if len(file_name.split(",")) > 0:
        file_list = file_name.split(",")
        image_filename = file_list[0]
    else:
        image_filename = file_name


    if os.environ.get('FLASK_CONFIG_TYPE')=='local':
        print("*** sleeping for 5 seconds *")
        time.sleep(5)

    logger_main.info(f"- /rincon_post_file respose with filename sent: {image_filename}") 

    return send_from_directory(os.path.join(config.get('DB_ROOT'),"rincon_files", \
        rincon_files_db_folder_name), image_filename)



if __name__=='__main__':
    app.run()



