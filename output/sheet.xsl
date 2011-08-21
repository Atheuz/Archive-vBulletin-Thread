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
                    <xsl:for-each select="thread/breadcrumbs/*">
                        <xsl:value-of select="."/>
                        <xsl:if test="position()!=last()">
                            <xsl:text> > </xsl:text>
                        </xsl:if>
                        <xsl:if test="position()=last()">
                            <xsl:text> ! </xsl:text>
                        </xsl:if>
                    </xsl:for-each>
                </h2>
                <table>
                    <tr>
                        <td>
                            <xsl:text>Locked: </xsl:text>
                            <xsl:value-of select="thread/locked"/>
                            <xsl:text> | </xsl:text>
                        </td>
                        <td>
                            <xsl:text>Pages: </xsl:text>
                            <xsl:value-of select="thread/pages"/>
                            <xsl:text> | </xsl:text>
                        </td>
                        <td>
                            <a>
                                <xsl:attribute name="href"><xsl:value-of select="thread/url"/></xsl:attribute>
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
                                            <xsl:value-of select="author"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="author"/>
                                    </a>
                                    <br />
                                    <xsl:text>Date: </xsl:text>
                                    <xsl:value-of select="date"/>
                                </td>
                                <td class="info2">
                                    <xsl:text>Post: </xsl:text>
                                    <xsl:value-of select="number"/>
                                    <br />
                                    <xsl:text>Page: </xsl:text>
                                    <xsl:value-of select="page"/>
                                    <br />
                                    <xsl:text>ID: </xsl:text>
                                    <xsl:value-of select="@id"/>
                                </td>
                                <td class="content">
                                    <xsl:copy-of select="content"/>
                                </td>
                            </tr>
                        </xsl:if>
                        <xsl:if test="position() mod 2 = 0">
                            <tr class="even">
                                <td class="info1">
                                    <a>
                                        <xsl:attribute name="href">
                                            <xsl:text>http://forums.somethingawful.com/member.php?action=getinfo&amp;username=</xsl:text>
                                            <xsl:value-of select="author"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="author"/>
                                    </a>
                                    <br />
                                    <xsl:text>Date: </xsl:text>
                                    <xsl:value-of select="date"/>
                                </td>
                                <td class="info2">
                                    <xsl:text>Post: </xsl:text>
                                    <xsl:value-of select="number"/>
                                    <br />
                                    <xsl:text>Page: </xsl:text>
                                    <xsl:value-of select="page"/>
                                    <br />
                                    <xsl:text>ID: </xsl:text>
                                    <xsl:value-of select="@id"/>
                                </td>
                                <td class="content">
                                    <xsl:copy-of select="content"/>
                                </td>
                            </tr>
                        </xsl:if>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>

