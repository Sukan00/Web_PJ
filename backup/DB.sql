PGDMP  ,                    }            DB    17.4    17.4     @           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            A           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            B           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            C           1262    16388    DB    DATABASE     j   CREATE DATABASE "DB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'th-TH';
    DROP DATABASE "DB";
                     postgres    false            �            1259    24940    advisor    TABLE     r   CREATE TABLE public.advisor (
    advisor_email character varying NOT NULL,
    advisor_name character varying
);
    DROP TABLE public.advisor;
       public         heap r       postgres    false            �            1259    24979    author    TABLE     {   CREATE TABLE public.author (
    au_id character varying NOT NULL,
    au_name character varying,
    report_id integer
);
    DROP TABLE public.author;
       public         heap r       postgres    false            �            1259    24957    report    TABLE     �  CREATE TABLE public.report (
    report_id integer NOT NULL,
    title character varying,
    intro character varying,
    year integer,
    category character varying,
    org character varying,
    type_org character varying,
    "position" character varying,
    path character varying,
    user_email character varying,
    advisor_email character varying,
    author character varying[]
);
    DROP TABLE public.report;
       public         heap r       postgres    false            �            1259    24956    report_report_id_seq    SEQUENCE     �   CREATE SEQUENCE public.report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.report_report_id_seq;
       public               postgres    false    220            D           0    0    report_report_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.report_report_id_seq OWNED BY public.report.report_id;
          public               postgres    false    219            �            1259    25004    report_type    TABLE     Z   CREATE TABLE public.report_type (
    report_id integer NOT NULL,
    type_name text[]
);
    DROP TABLE public.report_type;
       public         heap r       postgres    false            �            1259    24933    user    TABLE     �   CREATE TABLE public."user" (
    user_email character varying NOT NULL,
    password character varying NOT NULL,
    role character varying NOT NULL
);
    DROP TABLE public."user";
       public         heap r       postgres    false            �           2604    25090    report report_id    DEFAULT     t   ALTER TABLE ONLY public.report ALTER COLUMN report_id SET DEFAULT nextval('public.report_report_id_seq'::regclass);
 ?   ALTER TABLE public.report ALTER COLUMN report_id DROP DEFAULT;
       public               postgres    false    219    220    220            9          0    24940    advisor 
   TABLE DATA           >   COPY public.advisor (advisor_email, advisor_name) FROM stdin;
    public               postgres    false    218   z        <          0    24979    author 
   TABLE DATA           ;   COPY public.author (au_id, au_name, report_id) FROM stdin;
    public               postgres    false    221   $       ;          0    24957    report 
   TABLE DATA           �   COPY public.report (report_id, title, intro, year, category, org, type_org, "position", path, user_email, advisor_email, author) FROM stdin;
    public               postgres    false    220    -       =          0    25004    report_type 
   TABLE DATA           ;   COPY public.report_type (report_id, type_name) FROM stdin;
    public               postgres    false    222   �0       8          0    24933    user 
   TABLE DATA           <   COPY public."user" (user_email, password, role) FROM stdin;
    public               postgres    false    217   d1       E           0    0    report_report_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.report_report_id_seq', 42, true);
          public               postgres    false    219            �           2606    25386    author Au_id_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.author
    ADD CONSTRAINT "Au_id_pkey" PRIMARY KEY (au_id);
 =   ALTER TABLE ONLY public.author DROP CONSTRAINT "Au_id_pkey";
       public                 postgres    false    221            �           2606    24939    user User_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (user_email);
 <   ALTER TABLE ONLY public."user" DROP CONSTRAINT "User_pkey";
       public                 postgres    false    217            �           2606    24946    advisor advisor_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.advisor
    ADD CONSTRAINT advisor_pkey PRIMARY KEY (advisor_email);
 >   ALTER TABLE ONLY public.advisor DROP CONSTRAINT advisor_pkey;
       public                 postgres    false    218            �           2606    24966    report report_creator_key 
   CONSTRAINT     Z   ALTER TABLE ONLY public.report
    ADD CONSTRAINT report_creator_key UNIQUE (user_email);
 C   ALTER TABLE ONLY public.report DROP CONSTRAINT report_creator_key;
       public                 postgres    false    220            �           2606    24964    report report_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.report
    ADD CONSTRAINT report_pkey PRIMARY KEY (report_id);
 <   ALTER TABLE ONLY public.report DROP CONSTRAINT report_pkey;
       public                 postgres    false    220            �           2606    25395 (   report_type report_type_association_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY public.report_type
    ADD CONSTRAINT report_type_association_pkey PRIMARY KEY (report_id);
 R   ALTER TABLE ONLY public.report_type DROP CONSTRAINT report_type_association_pkey;
       public                 postgres    false    222            �           2606    24974     report report_advisor_email_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.report
    ADD CONSTRAINT report_advisor_email_fkey FOREIGN KEY (advisor_email) REFERENCES public.advisor(advisor_email);
 J   ALTER TABLE ONLY public.report DROP CONSTRAINT report_advisor_email_fkey;
       public               postgres    false    218    4762    220            �           2606    24969    report report_creator_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.report
    ADD CONSTRAINT report_creator_fkey FOREIGN KEY (user_email) REFERENCES public."user"(user_email);
 D   ALTER TABLE ONLY public.report DROP CONSTRAINT report_creator_fkey;
       public               postgres    false    4760    220    217            �           2606    25387    author report_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.author
    ADD CONSTRAINT report_id_fkey FOREIGN KEY (report_id) REFERENCES public.report(report_id) NOT VALID;
 ?   ALTER TABLE ONLY public.author DROP CONSTRAINT report_id_fkey;
       public               postgres    false    4766    220    221            �           2606    25009 2   report_type report_type_association_report_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.report_type
    ADD CONSTRAINT report_type_association_report_id_fkey FOREIGN KEY (report_id) REFERENCES public.report(report_id);
 \   ALTER TABLE ONLY public.report_type DROP CONSTRAINT report_type_association_report_id_fkey;
       public               postgres    false    220    222    4766            9   �  x�}U�N�0���"O`	�}�I���&��P���eH@�Jh0��T��S��漍e��14TBƱ��s�=�:Y&�8���Ղ��Z\�<�v��QrΕ�RrJ�.�\)y��-};J�����3%�*?R�&S%���$~=�#��
����Q򇒹��Jީ���Օ�#lӼ���a���Y}_��Լ8���n>*�Vr>�-zNX�*?��\@G���D��������-�y�����bxs�ᆹ��q���V@���("5/-)b��t�LD>O��l�G�cE�C��'�s�0����ȼZWxq\HY�t���بy�Ց�X���}��.��S���i�M}����A��1Aހ�� ��Tv2�֚�B��!�MHɑk���Gd��H���K��F���Y�r� :6�����=�>c�N[tE(�<��I�����I�S����S�����\����B�Hc��oi���t���t�+��_�t��:���H�#K�n�G�-�6�ۦ��K��6U��\��>��M�Fb+�#��&Ap$���	�H"�Y�5���P� �����5�K֍�z#�9��=��;��:��lq�e�4�(�ޕG����_,i5,*ca�d~*Od�[�'o�fZ*,��_pO��tH�]_��@]+�0x{�з�x�@�\��ߢ!�ma�������W����P�xJ��ߠ8���-��$t�p��"L�Y���_����k�뇎�M@RO(}������X\���c�������V��/�&ףf�hx����M%�j�ll����"]o?m��;HE�pn�:z���(+�~���x��"�-x���6��o\zn2r���e2r�t��4N���o�L�#l{�k3�0d8c�?��x�      <   �  x��Yk��F�=s
� ��1�%r�=�2A��,�&@�E"<1�h�����U|�\!�U]��M{#�F���\]��N�a7���]S-���T���4�[S}n��:6�͛j�ԟ���ɫj���kSl��������r����TbGq±G�N,Z7�!hj��O^K�8ía��bE	Gxש��4U�T� Ĭ���
b�޵"k�����;_�j#�pW�M���wq� q/�gY����������%Tw?�P$��r7�1G	��CS�
�NR%I� ��[	� �, ��,!�e�-�����P��_}X�G9�R�R-�N[5�:\�>ɁV&Ur�B(�ʶ��޽u��D�g��/R���{f�	
�#���:20q��+��R���о����V^:Ƙ@u�U,���Տ��#%�A�@\n�\�ok@ނ�?�3�~/�|x*f�Gꕟ��Z�=��)a�<z�+J��3~�?P�A�}T
Ƣxň6``��D�C-(uE6�)���Ѕpq�w���X'�
�J��ύ6��:�
^W�;,���)Zጳ�jv̎ˠbP���bT��f@�[��2i�&��y���<�� b&���gS��;0�g�	��lM���C-�9U��C2l��6le9�P���1�AJ��P�*}��4`y�M>T��X�P���;���a����c��"Җ\vJ
C-�L�{a&N�Ї��cJ͕�t�n|��M�/J�5��3yO�����	��C�g�݋4E,|�����խ�&�9%؁���n��>0�����ɽ0��h+#�3&����M�J��P�����`,iV��p�5�T.j;Y��o����TX\����ٌJ�6��Q��mW�������S�ũ��}uM2.�|�/�䚋S*\PI����-��?����#d�y �8��_)���T�e*pK����<_�]}��n���Ӗ�(���j�����ڊX����G|���K�%9�3z��l���������:0GЊ�4��������ԟw53��iDr� ؖ���
SVĖx���'���}�.�O *W�F�bY+<��u��ia�%��ӕ � vTRɢ���+]��|_K������W�zGF ڂ:�u'����-�!�2��m�X@��$����ebEyez]î�Q,��&���*Ab^,�`�3��xD�����
�M(P�u�+f���!�ղ��M���5ꑲ�ұg�3��b�UG�]bST��
�fa��Z+�1�� �W��ĭ���ߵn2 f��U�1�`�ā�yN�%�j����&!��Gh��n��ǜ?�� �#́L�K �}�rѥߴ%��=M2��U�����O#YΑ0sKePi!�c��ki�֤屣!��;��F��{^_����0������~'��nxr]�K����!�T�|i�����?�
	Y���k�5��J����B
�z������R�J�2��א8t��i�Wۆ(q���#���4�psFj����*'z�ﱮS�4�90W5
� ����hf����Q��Pw�Wc�-��5��b� @��ӥmiљЎ�سs+��̥���t���%Y:���42��;��/�䍪�/�Dz�U�΄��;B�2>�P�f��ʉ�׳�P$�Y�'6w�}���F�扺���3�4�?�d3*�J� y�y�g���:G5<��mJ��6P�o&(z͆�V��B��=`�*i�a���졒�]Q)-/�?�M�J)���|يT���g1��!�B��G^�g��%(�2T�@.��g-��g�p���*,�3�a;�3Տk�D����2+��Ъ$K��-XH���VU���V+�ye���G��,�"��K[ъ�4	=�'��d�F�C����W�O'_��)�������Ԟy�������%c ҊH����t���CW���n蘵"v��AuF�JՖY ~j+iR���=��뢛�C��qC��p)� �R02���:y()��j�c����=�D��U��U{�>��M(����$j9�ɯ���at1q[���Yl�������(��J7�[����,�
vD�-��ԀuB�X�[�E�ď��eS��|hc�X�@�h��#.fO�(dxoB}0�n�0 �8���ï�[���>�ߡ��gb'!�=JA����Li��Z�T�5R�eҼ�U�'��p��iA׎�mwI��������o��      ;   �  x���O��6���O��^�A����醆�lY��m�Ȓ�V׶\I�e(�6���KJɱiKhK�-�z��?J�53ٙe�� K�O�O�'�'�{�BH0�_M�����4~3�M㫝����o�8�|9��M�?�������}�_��?��;�~;����M%i�^r�����.���7�	{~^�F~"r��e��Bp��R\Ɣc�(MdDӢX��
҄$$���V�f����AôY�z����m���&���/h<�����FZtj�P�)ݡgVu��Zu=��t�,Q��j6]��B6��̡~��E��#��Y����Hu$�YO�:1XgV3�"��>8ziN�q�;��,/x�Cˎ5+;8i�;�R��1)b��p,H��8L0�2Q���ŷ��$�T��X��W���x���C	�f+�4���ʦk~�Ɵ���i|9Kq���^�?|��ܾy�__x�^���,�QH�] ���^mx:~>$�8i�S���RD��`��".FCY�"�e@�po�B�Y�б�v-̹��"��A�Ji��Qn���F��?�N��9�#�-�b}c-��s�R`�����-�n��-�1ﲱ�BC`������T��B�	�b�☄!1�<N aEv $��K�� �- �=@���h��<��#ձn^z��%ZZ+�ma���WF�({���Sm\��m�Vm6���0d�4�6M�.��i���9e��09�ա֜��@�]��z�=2z ��T���w��NY�(!�� �UU`�2����X�Qȳ��0}��B�(���T_K�:��Rj��z׃n�x�f��*� �@!�d���?hy��&�( `E|��Js� ��>���\�����.���g%pӈ�z�IT⢠eJbJ�d�z�3��{WF\^����^i4�9_���hR      =   �   x�36�V�Q�Qw�T�QRw�LWpI,ITW��2� ���&%g U��'��� �I9��@5�@5`�\&@vprb��sFjb	H�(�\��ZT����l�+.-J�KN��`��;;���`��;6>���`Ǫ;v<�1���6��=... qK<\      8   �  x�m�KnT1E�݋����5c!LZM�D$A
���$�@� N���Q�|�v�~~�1�ַm�?|~y�<ߝ�w�������������[(F�j5A�C�}���Pu�,Vc�n�wfߛQT�����+����c��v�+ERըJJ�HT5��j�D��,�Ƽ�x�"�B� ]���S���ӯ�ʊ)���3�\B�jI�)������W0��X�Xu��RU�*���J�k�R�妥j؊�+9�)��rVS$%w;EP����ǶɊ)��:��\mt�ٻ����.{LԐ�+ER�}��ͼo���j�CmY���"~��Uo(�P�kқ��Aى�<�}�)�'R5�L�Hʲ��~I�S$e�c�y�~������J�u���<v�+ERR���p�R�II�_ú�`�֑;�Xk1����>4��㦎֭�լ�W��d��[;�T;ER���l�}���Q���_���4�'�������� ���I�A�ܱ8w,�;�e7m�-{�߯5ůI���[V��
��t56q"EP�j�հ_Z�6����Y!8+����}�.7-ERR���6�g���I�o��=�ؼ]8o�p��U$u��UU,Va,�VWT�}�"(��]�T�d�}�R������������������.����������x��e��     