<?xml version='1.0' encoding='utf-8'?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
                <style type="text/css">
                    body {
                        color:#DDDDDD;
                        background-color:#434343;
                        text-align:justify;
                    }
                    * {
                        font-family: Calibri;
                    }
                    a {
                        color:#4F94CD;
                    }
                    a:hover {
                        text-decoration:none;
                    }
                    a:active {
                        color:#666666;
                        text-decoration:none;
                    }
                    td {
                        background-color:#393939;
                    }
                    td.author {
                        width:5%;
                        border: 1px solid black;
                    }
                    td.date {
                        width:10%;
                        border: 1px solid black;
                    }
                    td.content {
                        padding:0.33em;
                        width:85%;
                        border: 1px solid black;
                    }
                    p {
                        margin:0.25em 0;
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
                <p>
                    <xsl:text>Locked: </xsl:text>
                    <xsl:value-of select="thread/locked"/>
                </p>
                <p>
                    <xsl:text>Pages: </xsl:text>
                    <xsl:value-of select="thread/pages"/>
                </p>
                <a>
                    <xsl:attribute name="href"><xsl:value-of select="thread/url"/></xsl:attribute>
                    <xsl:text>Thread URL</xsl:text>
                </a>

                <table>
                    <xsl:for-each select="thread/posts/post">
                        <tr>
                            <td class="author">
                                <xsl:value-of select="author"/>
                                <br />
                                <xsl:text>Date: </xsl:text>
                                <xsl:value-of select="date"/>
                            </td>
                            <td class="date">
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
                                <xsl:value-of select="content"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
