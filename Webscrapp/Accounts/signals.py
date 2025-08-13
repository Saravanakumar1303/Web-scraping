from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from Accounts.models import job, JobQueue

@receiver(post_save, sender=job)
def job_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            print(f"[Signal] New Job created: {instance.url}, Priority: {instance.priority}, Status: {instance.status}")
            
            job_queue = JobQueue.objects.create(job=instance, queue=1)
            
            print(f"[Signal] JobQueue created for Job: {instance.url}, Queue: {job_queue.queue}")
        
        except Exception as e:
            print(f"[Signal Error] Failed to create JobQueue: {e}")

@receiver(post_delete, sender=job)
def job_post_delete(sender, instance, **kwargs):
    try:
        print(f"[Signal] Job deleted: {instance.url}, Priority: {instance.priority}, Status: {instance.status}")
        
        job_queue = JobQueue.objects.get(job=instance)
        job_queue.delete()

        print(f"[Signal] JobQueue deleted for Job: {instance.url}, Queue: {job_queue.queue}")

    except JobQueue.DoesNotExist:
        print(f"[Signal] No JobQueue found for Job: {instance.url}")

    except Exception as e:
        print(f"[Signal Error] Failed to delete JobQueue: {e}")