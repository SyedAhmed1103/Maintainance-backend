from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


# =========================================================
# USER MANAGER
# =========================================================

class UserManager(BaseUserManager):

    def create_user(
        self,
        email,
        mobile,
        password=None,
        **extra_fields
    ):

        if not email:
            raise ValueError(
                "Email is required."
            )

        if not mobile:
            raise ValueError(
                "Mobile is required."
            )

        email = self.normalize_email(
            email
        )

        user = self.model(
            email=email,
            mobile=mobile,
            **extra_fields
        )

        user.set_password(
            password
        )

        user.save(
            using=self._db
        )

        return user

    def create_superuser(
        self,
        email,
        mobile,
        password,
        **extra_fields
    ):

        extra_fields.setdefault(
            "user_type",
            User.UserType.ADMIN
        )

        extra_fields.setdefault(
            "is_staff",
            True
        )

        extra_fields.setdefault(
            "is_superuser",
            True
        )

        extra_fields.setdefault(
            "is_active",
            True
        )

        return self.create_user(
            email=email,
            mobile=mobile,
            password=password,
            **extra_fields
        )


# =========================================================
# USER
# =========================================================

class User(AbstractUser):

    class UserType(models.TextChoices):

        ADMIN = (
            "admin",
            "Admin"
        )

        OWNER = (
            "owner",
            "Owner"
        )

        TENANT = (
            "tenant",
            "Tenant"
        )

        COMMITTEE = (
            "committee",
            "Committee"
        )

        SECURITY = (
            "security",
            "Security"
        )

        MANAGER = (
            "manager",
            "Manager"
        )

    # -----------------------------------------------------
    # AUTH
    # -----------------------------------------------------

    id = models.BigAutoField(
        primary_key=True
    )

    username = None

    email = models.EmailField(
        unique=True,
        db_index=True
    )

    mobile = models.CharField(
        max_length=15,
        unique=True,
        db_index=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "mobile"
    ]

    objects = UserManager()

    # -----------------------------------------------------
    # PERSONAL INFO
    # -----------------------------------------------------

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # ROLE
    # -----------------------------------------------------

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.OWNER,
        db_index=True
    )

    # -----------------------------------------------------
    # SOCIETY MAPPING
    # -----------------------------------------------------

    building = models.ForeignKey(
        "building.Building",
        on_delete=models.CASCADE,
        related_name="users"
    )

    flat = models.ForeignKey(
        "flats.Flat",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    is_verified = models.BooleanField(
        default=False
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    # -----------------------------------------------------
    # SOFT DELETE
    # -----------------------------------------------------

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # AUDIT
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        db_table = "users"

        ordering = [
            "-created_at"
        ]

        indexes = [

            models.Index(
                fields=[
                    "email"
                ]
            ),

            models.Index(
                fields=[
                    "mobile"
                ]
            ),

            models.Index(
                fields=[
                    "user_type"
                ]
            ),

            models.Index(
                fields=[
                    "building"
                ]
            ),

            models.Index(
                fields=[
                    "flat"
                ]
            ),

            models.Index(
                fields=[
                    "is_active"
                ]
            ),

            models.Index(
                fields=[
                    "created_at"
                ]
            ),
        ]

    # -----------------------------------------------------
    # HELPERS
    # -----------------------------------------------------

    def save(
        self,
        *args,
        **kwargs
    ):

        if self.email:

            self.email = (
                self.email
                .lower()
                .strip()
            )

        if self.mobile:

            self.mobile = (
                self.mobile
                .replace(" ", "")
                .strip()
            )

        super().save(
            *args,
            **kwargs
        )

    @property
    def full_name(
        self
    ):

        return (
            f"{self.first_name} "
            f"{self.last_name or ''}"
        ).strip()

    @property
    def is_admin(
        self
    ):

        return (
            self.user_type
            == self.UserType.ADMIN
        )

    @property
    def avatar(
        self
    ):

        try:

            from django.contrib.contenttypes.models import ContentType
            from apps.media_manager.models import Media

            content_type = (
                ContentType.objects.get_for_model(
                    self.__class__
                )
            )

            return (
                Media.objects.filter(
                    content_type=content_type,
                    object_id=self.id,
                    category=Media.Category.AVATAR,
                    is_active=True
                )
                .first()
            )

        except Exception:

            return None

    def __str__(
        self
    ):

        return (
            f"{self.full_name} "
            f"({self.user_type})"
        )