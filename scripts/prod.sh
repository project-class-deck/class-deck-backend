gunicorn backend.wsgi -w 3 -b 0.0.0.0:8000 --error-logfile /home/ec2-user/logs/error.log --access-logfile /home/ec2-user/logs/access.log
