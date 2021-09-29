import pytest
from django.urls import reverse
from students.models import Course


@pytest.mark.django_db
def test_course(client, student_factory, course_factory):

    student_factory(_quantity=1)
    course_factory(_quantity=1)
    cor = Course.objects.first()
    url = reverse('courses-detail', args=(cor.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == cor.id

@pytest.mark.django_db
def test_courses_list(client, student_factory, course_factory):
    student_factory(_quantity=3)
    course_factory(_quantity=3)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_course_id(client, course_factory):
    course_factory(_quantity=4)
    url = reverse('courses-list')
    x = Course.objects.all()
    response = client.get(url, data={'id': x[0].id})
    assert response.data[0].get('id') == x[0].id

@pytest.mark.django_db
def test_course_delete(client, course_factory):
    course_factory(_quantity=1)
    cor = Course.objects.first()
    url = reverse('courses-detail', args=(cor.id,))
    response = client.delete(url, data={'id': f'{cor.id}'})
    assert response.status_code == 204

@pytest.mark.django_db
def test_course_patch(client, course_factory):
    course_factory(_quantity=1)
    cor = Course.objects.first()
    url = reverse('courses-detail', args=(cor.id,))
    response = client.patch(url, data={'name': '777'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_courses_name(client, course_factory):
    course_factory(_quantity=4)
    x = Course.objects.all()
    url = reverse('courses-list')
    response = client.get(url, data={'name': x[0].name})
    assert response.data[0].get('name') == x[0].name

@pytest.mark.django_db
def test_courses_post(client):
    x = {'name': 'Course'}
    url = reverse('courses-list')
    response = client.post(url, data=x)
    assert response.status_code == 201

