<?xml version='1.0' encoding='utf-8'?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <html>
            <head>
                <style type="text/css">
                    body {
                        color:GhostWhite;
                        background-color:black;
                        text-align:justify;
                    }
                    * {
                        font-family:Calibri;
                    }
                    a {
                        color:GhostWhite;
                    }
                    a:hover {
                        text-decoration:none;
                    }
                    a:active {
                        color:GhostWhite;
                        text-decoration:none;
                    }
                    tr.odd {
                        background-color:#778899;
                    }
                    tr.even {
                        background-color:#92A6BB;
                    }
                    td.info1 {
                        padding:0.33em;
                        width:12.5%;
                        border: 1px solid black;
                    }
                    td.info2 {
                        padding:0.33em;
                        width:6.5%;
                        border: 1px solid black;
                    }
                    td.content {
                        padding:0.5em;
                        width:80%;
                        border: 1px solid black;
                        }
                    p {
                        margin:0.25em 0;
                    }
                    h2 {
                        text-align:center;
                    }
                </style>
            </head>
            <body>
                <h2>
                    <xsl:value-of select="thread/breadcrumbs/@thread_forum"/>
                    <xsl:text> > </xsl:text>
                    <xsl:value-of select="thread/breadcrumbs/@thread_board"/>
                    <xsl:text> > </xsl:text>
                    <xsl:value-of select="thread/breadcrumbs/@thread_subboard"/>
                    <xsl:text> > </xsl:text>
                    <xsl:if test="thread/breadcrumbs/@thread_subsubboard/text() != None">
                        <xsl:value-of select="thread/breadcrumbs/@thread_subsubboard"/>
                        <xsl:text> > </xsl:text>
                    </xsl:if>
                    <xsl:value-of select="thread/breadcrumbs/@thread_title"/>
                </h2>
                <table>
                    <tr>
                        <td>
                            <xsl:text>Locked: </xsl:text>
                            <xsl:value-of select="thread/@thread_locked"/>
                            <xsl:text> | </xsl:text>
                        </td>
                        <td>
                            <xsl:text>Pages: </xsl:text>
                            <xsl:value-of select="thread/@thread_page_count"/>
                            <xsl:text> | </xsl:text>
                        </td>
                        <td>
                            <a>
                                <xsl:attribute name="href"><xsl:value-of select="thread/@thread_url"/></xsl:attribute>
                                <xsl:text>Thread URL</xsl:text>
                            </a>
                        </td>
                    </tr>
                </table>
                <table>
                    <xsl:for-each select="thread/posts/post">
                        <xsl:if test="position() mod 2 = 1">
                            <tr class="odd">
                                <td class="info1">
                                    <a>
                                        <xsl:attribute name="href">
                                            <xsl:text>http://forums.somethingawful.com/member.php?action=getinfo&amp;username=</xsl:text>
                                            <xsl:value-of select="@post_author"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="@post_author"/>
                                    </a>
                                    <br />
                                    <xsl:text>Regdate: </xsl:text>
                                    <xsl:value-of select="@post_author_regdate"/>
                                    <br />
                                    <xsl:text>Date: </xsl:text>
                                    <xsl:value-of select="@post_date"/>
                                </td>
                                <td class="info2">
                                    <xsl:text>Post: </xsl:text>
                                    <xsl:value-of select="@post_thread_number"/>
                                    <br />
                                    <xsl:text>Page: </xsl:text>
                                    <xsl:value-of select="@post_thread_page"/>
                                    <br />
                                    <xsl:text>ID: </xsl:text>
                                    <xsl:value-of select="@post_id"/>
                                </td>
                                <td class="content">
                                    <xsl:value-of select="content" disable-output-escaping="yes"/>
                                </td>
                            </tr>
                        </xsl:if>
                        <xsl:if test="position() mod 2 = 0">
                            <tr class="even">
                                <td class="info1">
                                    <a>
                                        <xsl:attribute name="href">
                                            <xsl:text>http://forums.somethingawful.com/member.php?action=getinfo&amp;username=</xsl:text>
                                            <xsl:value-of select="@post_author"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="@post_author"/>
                                    </a>
                                    <br />
                                    <xsl:text>Regdate: </xsl:text>
                                    <xsl:value-of select="@post_author_regdate"/>
                                    <br />
                                    <xsl:text>Date: </xsl:text>
                                    <xsl:value-of select="@post_date"/>
                                </td>
                                <td class="info2">
                                    <xsl:text>Post: </xsl:text>
                                    <xsl:value-of select="@post_thread_number"/>
                                    <br />
                                    <xsl:text>Page: </xsl:text>
                                    <xsl:value-of select="@post_thread_page"/>
                                    <br />
                                    <xsl:text>ID: </xsl:text>
                                    <xsl:value-of select="@post_id"/>
                                </td>
                                <td class="content">
                                    <xsl:value-of select="content" disable-output-escaping="yes"/>
                                </td>
                            </tr>
                        </xsl:if>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>

