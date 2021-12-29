Configuring Groups
------------------

To display the wagtail-localize panel, users have to subscribe to a root
lang page and allow permissions.

The first things to do is to create a group for that.

Example with a french translation:

Create a new group
~~~~~~~~~~~~~~~~~~

In the wagtail `Settings / Groups` menu, add a new group using the 
button `Add a group`.

.. image:: ./screen_1.png
   :alt: Add a group


Then, set the name of the group.

.. image:: ./screen_2.png
   :alt: Name the group "FR Translators"


Then, check the boxes `View the localize panel on the admin`
and `Receive email on new translations`.

.. image:: ./screen_3.png
   :alt: Check the boxes


Then, choose the root page of the language, and check the "edit" permissions.

.. image:: ./screen_4.png
   :alt: Check the edit on language root page.


Then, add save the group using the button on the bottom of the page.

.. image:: ./screen_5.png
   :alt: Save the new group.


To finalize your group, users must be added in the group.

Edit users under the menu `Settings / Users`

.. image:: ./screen_6.png
   :alt: List users.

And add the new role tab of the user, check the box of the new group and
click the save button.

.. image:: ./screen_7.png
   :alt: Add the role to the user.


Now users in the group have the panel of translations in their home page:

.. image:: ./screen_8.png
   :alt: Add the role to the user.

if the checkbox `Receive email on new translations` is checked,
every time the page in the source lang is published, an email will be
sent to users to notify them of the incoming translations.


.. important::

   This plugin automatically does the "synchronize translations", so it is now useless
   to use the `Sync translated pages`
