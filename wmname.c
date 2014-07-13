#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <xcb/xcb.h>
#include <xcb/xproto.h>

#include "wmname.h"

typedef struct xconn_t {
	xcb_connection_t *conn;
	xcb_screen_t     *screen;
	int               screen_num;
} xconn_t;

int main(void) {
  printf("Trying to connect...\n");
  xconn_t* conn = connect_x();
  if (conn == 0)
    printf("Error trying to connect\n");

  printf("Setting screen\n");
  int res1 = set_screen(conn);
  if (res1 != 0)
    printf("Error trying to set screen\n");

  printf("Trying to set name...\n");
  const char *texto = "Funciona\0";
  int res = set_wm_name(conn, texto);
  if (res != 0)
    printf("Error trying to set name\n");

  printf("Disconnecting...\n");
  disconnect_x(conn);
  return 0;
}

xconn_t *connect_x(void)
{
  printf("Connecting...\n");

	xconn_t *xconn = malloc(sizeof(xconn_t));

	if (xconn == NULL)
		return NULL;

	xconn->conn = xcb_connect(NULL, &xconn->screen_num);
	if (xcb_connection_has_error(xconn->conn))
		return NULL;

	return xconn;
}

void disconnect_x(xconn_t *xconn)
{
  printf("Disconnecting...\n");
	xcb_disconnect(xconn->conn);
	free(xconn);
}

int set_screen(xconn_t *xconn)
{
	xcb_screen_iterator_t it;
	int screen_num = xconn->screen_num;

	xconn->screen = NULL;
	it = xcb_setup_roots_iterator(xcb_get_setup(xconn->conn));
	for (; it.rem; xcb_screen_next(&it), screen_num--) {
		if (screen_num == 0) {
			xconn->screen = it.data;
			break;
		}
	}
	if (xconn->screen == NULL)
		return -1;

	return 0;
}

int set_wm_name(xconn_t *xconn, const char *name)
{
	xcb_void_cookie_t cookie;

	cookie = xcb_change_property_checked(xconn->conn,
					     XCB_PROP_MODE_REPLACE,
					     xconn->screen->root,
					     XCB_ATOM_WM_NAME,
					     XCB_ATOM_STRING,
					     8,
					     strlen(name),
					     name);

	if (xcb_request_check(xconn->conn, cookie) != NULL)
		return -1;

	return 0;
}

int myprint(char *text)
{
  printf("Printing: ");
  printf("%s", text);
  return 0;
}

